# Design Diagrams

Written in [Mermaid](https://mermaid.js.org/); they render on GitHub and in the VS Code Markdown preview.

## Class diagram

```mermaid
classDiagram
    class Person {
        <<abstract>>
        Long id
        String name
    }
    class Member {
        MemberType type
        getBorrowLimit()
    }
    class AppUser {
        String username
        String passwordHash
        Role role
    }
    class Book {
        Long id
        String title
        String author
        String isbn
        issueTo(Member)
        markReturned()
        isAvailable()
    }
    class BorrowService {
        issue()
        giveBack()
    }
    class LibraryException {
        <<abstract>>
        HttpStatus status
    }

    Person <|-- Member
    Person <|-- AppUser
    Book "0..*" --> "0..1" Member : borrower
    BorrowService ..> Book : updates
    BorrowService ..> Member : checks limit
    BorrowService ..> LibraryException : throws
```

`MemberType` is `STUDENT` (limit 3) or `FACULTY` (limit 5). `Role` is `ADMIN`, `LIBRARIAN` or `MEMBER`.

## Activity diagram: sign in

```mermaid
flowchart TD
    A([Start]) --> B[Enter username and password]
    B --> C{Credentials valid?}
    C -- No --> D[Show error] --> B
    C -- Yes --> E[Show views for the user's role]
    E --> F([End])
```

## Activity diagram: issue a book

```mermaid
flowchart TD
    A([Start]) --> B[Pick a book and a member]
    B --> C{Book available?}
    C -- No --> X[Show error]
    C -- Yes --> D{Member under borrow limit?}
    D -- No --> X
    D -- Yes --> E[Issue the book]
    E --> F[Show book as issued]
    F --> G([End])
    X --> G
```
