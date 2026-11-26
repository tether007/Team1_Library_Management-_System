from common import (bullets, callout, code, h1, h2, h3, numbered, p, qa, snip, table)

B = "backend/src/main/java/com/team1/library/"
T = "backend/src/test/java/com/team1/library/"
F = "frontend/src/"


def testing():
    out = h1("19. Testing")
    out += p("Tests turn the requirements into repeatable checks. There are **65 automated tests**: 23 on the backend (JUnit 5) and 42 on the frontend (Vitest).")
    out += h2("19.1 Backend: JUnit 5")
    out += table([
        ["Kind", "Class", "Tests", "What it proves"],
        ["Unit test (Mockito)", "BorrowServiceTest", "7", "Lending rules in isolation: issue marks the book borrowed; already issued is rejected; student limit 3; faculty may hold 5; unknown book and member; return makes the book available; returning an available book is rejected"],
        ["Integration (full Spring context + MockMvc)", "LibraryApiIntegrationTest", "15", "Authentication (3), role rules, paging, sorting, search, bad sort field, add book, duplicate ISBN, validation message, issue/return flow, borrow limit, 404s, and that the cache fills and is cleared"],
        ["Smoke", "LibraryApplicationTests", "1", "The application context starts (all beans wire up)"],
    ], [22, 24, 6, 48], small=True)
    out += snip(T + "service/BorrowServiceTest.java", "@ExtendWith(MockitoExtension.class)", "private Member student;", max_lines=24)
    out += snip(T + "service/BorrowServiceTest.java", "void issueEnforcesTheStudentLimit", None, max_lines=12, skip=0)
    out += bullets([
        "`@Mock` replaces the two repositories with fakes; `@InjectMocks` builds `BorrowService` and passes them into its constructor. **This works only because the class uses constructor injection.**",
        "No Spring, no database: the test runs in milliseconds.",
        "AssertJ (`assertThat`, `assertThatThrownBy`) reads like English.",
    ])
    out += snip(T + "LibraryApiIntegrationTest.java", "@SpringBootTest", "private CacheManager cacheManager;", max_lines=28)
    out += snip(T + "LibraryApiIntegrationTest.java", "void memberCannotAddBooksOrIssueThem", None, max_lines=10, skip=0)
    out += bullets([
        "`@SpringBootTest` starts the real application context (security filters, JPA, H2, seeded data).",
        "`@AutoConfigureMockMvc` provides `MockMvc`, which sends requests through the whole Spring stack **without opening a network port**.",
        "`httpBasic(\"member\", \"member123\")` (from spring-security-test) adds the Basic header, so the real security rules are exercised.",
        "`@Transactional` on the test class rolls back each test's changes, so tests do not influence each other. A `@BeforeEach` clears the cache.",
        "`jsonPath(\"$.message\")` asserts on the JSON body.",
    ])
    out += h2("19.2 Frontend: Vitest")
    out += table([
        ["Test file", "Tests", "Covers"],
        ["features/auth/auth.test.jsx", "5", "login success saves the session; wrong password shows the backend message; logout clears; permission table; login page error"],
        ["features/books/books.test.jsx", "6", "list stored with paging info; duplicate ISBN message; add-book flow; hidden form for members; next page and sort requests; search resets to page 0"],
        ["features/members/members.test.jsx", "5", "load members; 403 message; admin adds a member; librarian has no form; sort by type"],
        ["features/borrow/borrow.test.jsx", "3", "issue and return update the list; rule violation shown; issue flow on the page; asks for 100 rows"],
        ["features/pagination/pagination.test.jsx", "7", "page state conversion; sort toggling; Pager enable/disable and callbacks; SortHeader aria-sort"],
        ["features/navigation/navigation.test.jsx", "6", "tabs per role; navbar contents; profile photo below Sign out for all three roles; tab switch and sign-out"],
        ["features/profile/avatar.test.jsx", "2", "photo label and size"],
        ["App.test.jsx", "3", "login page when signed out; member lands on books with no staff tabs; sign-out returns to login"],
        ["app/localCache.test.js", "5", "restore, wipe, ignore bad shape, write/clear on change, clearCache"],
    ], [34, 8, 58], small=True)
    out += snip(F + "features/books/books.test.jsx", "vi.mock('../../api/libraryApi')", None, max_lines=20)
    out += bullets([
        "`vi.mock('../../api/libraryApi')` replaces the whole API module with automatic fakes. Each test decides what a call returns, for example `libraryApi.getBooks.mockResolvedValue(pageOf([...]))`.",
        "Frontend tests therefore check **how the UI and the store react**; the **business rules** are tested on the backend where they live.",
        "React Testing Library finds elements the way a user does (by label or role) and `user-event` types and clicks like a person.",
        "`test/setup.js` clears sessionStorage and localStorage after each test; `mockReset: true` in the config clears mock state between tests.",
    ])
    out += snip(F + "test/helpers.jsx", "export const apiError", None, max_lines=22)
    out += h2("19.3 How to run")
    out += table([
        ["Where", "Command", "Result"],
        ["backend/", "`mvnw.cmd test`", "Runs 23 tests; report in target/surefire-reports"],
        ["frontend/", "`npm test`", "Runs 42 tests once (no watch mode)"],
        ["frontend/", "`npm run lint`", "ESLint check"],
        ["frontend/", "`npm run build`", "Production build; fails if the code does not compile"],
    ], [20, 30, 50])
    return out


def oop():
    out = h1("20. Object-oriented and design principles mapped to the code")
    out += table([
        ["Principle", "Where it is used", "Explanation"],
        ["Encapsulation", "`Book`, `Member`, `AppUser`: private fields, no setters", "State changes only through meaningful methods (`issueTo`, `markReturned`); availability is derived, so it cannot be inconsistent"],
        ["Abstraction", "`Person` (abstract class); repository interfaces; `PageResponse`", "Callers see what something does, not how: you call `findById`, not SQL"],
        ["Inheritance", "`Person` -> `Member`, `AppUser`; `LibraryException` -> six exceptions; `RuntimeException`", "Shared fields and behaviour in the parent; children add their own"],
        ["Polymorphism", "`GlobalExceptionHandler.handleLibrary(LibraryException)`; `UserDetailsService`, `PasswordEncoder` interfaces", "One handler method serves every subclass; Spring Security depends on interfaces and receives our implementations"],
        ["Interfaces", "`JpaRepository`, `UserDetailsService`, `AuthenticationEntryPoint`, `AccessDeniedHandler`, `ApplicationRunner`, `BorrowCount`", "A contract that a class promises to fulfil; lets the framework call our code"],
        ["Constructors", "Public constructors with arguments; `protected` no-arg constructors for JPA; `super(name)` chaining", "Objects are created in a valid state; JPA gets the empty constructor it needs without exposing it"],
        ["Method overriding", "`@Override` of `loadUserByUsername`, `commence`, `handle`, `run`", "We replace default behaviour defined by an interface"],
        ["Method overloading", "Not required by any feature; not forced into the code", "If asked: overloading means the same method name with different parameter lists. A search overload such as `search(title)` and `search(author, year)` could be added to `BookService`"],
        ["Records (immutability)", "All DTOs", "Immutable value objects without boilerplate"],
        ["Exceptions as part of the design", "`exception/` package", "Errors are named business concepts, not return codes"],
    ], [20, 38, 42], small=True)
    out += h2("20.1 SOLID in one table")
    out += table([
        ["Principle", "Example"],
        ["Single Responsibility", "`BorrowService` lends and returns; `BookService` searches and adds; `SecurityErrorHandler` only writes error JSON"],
        ["Open / Closed", "A new member type is a new enum constant with its limit; no `if` chain to edit"],
        ["Liskov Substitution", "Anything that takes a `Person` works with `Member` or `AppUser`; any `LibraryException` is handled the same way"],
        ["Interface Segregation", "Small, focused interfaces: the repositories each expose only their own queries; `BorrowCount` has two getters"],
        ["Dependency Inversion", "Services depend on repository **interfaces** and receive them by injection; they never construct a concrete database class"],
    ], [24, 76])
    out += p("Other habits: **DRY** (`createApiThunk`, `createStore`, one `can()` function), **YAGNI** (no unused abstractions, no speculative features), "
             "**fail fast** (validation before work, rules checked before changes).")
    return out


def decisions():
    out = h1("21. Decision log: what was used, and what was not, and why")
    out += p("Evaluators often ask 'why not X?'. This chapter has the answer for each major choice.")
    out += h2("21.1 Backend")
    out += table([
        ["Topic", "Used", "Not used", "Reason"],
        ["Database", "H2 in memory", "MySQL / PostgreSQL / H2 file", "Requirement: do not persist data. Zero install. Because JPA is used, switching later is a URL and driver change"],
        ["Schema creation", "Hibernate `create-drop`", "Flyway / Liquibase migrations", "No persistent schema to evolve"],
        ["Data access", "Spring Data JPA", "JdbcTemplate, MyBatis, raw JDBC", "`@Entity` is required; derived queries and paging come free"],
        ["Authentication", "HTTP Basic + database users", "JWT, OAuth2, form login with sessions", "Requested approach. Stateless and simple. JWT needs a signing key, expiry and refresh logic; sessions need CSRF and server memory"],
        ["Password storage", "BCrypt", "Plain text, MD5, SHA-256", "Salted, deliberately slow, adaptive"],
        ["Authorization", "URL rules in SecurityConfig", "`@PreAuthorize` method security", "One visible table of rules is easier to review; method security can be added later"],
        ["API objects", "Record DTOs", "Returning entities directly", "Avoid leaking `passwordHash`, lazy-loading errors and coupling JSON to the schema"],
        ["Mapping", "Static `from` methods", "MapStruct / ModelMapper", "Only a few tiny mappings; a library would be heavier than the code"],
        ["Boilerplate", "Records and explicit code", "Lombok", "No annotation-processing magic; code is exactly what is read"],
        ["Dependency injection", "Constructor injection", "Field `@Autowired`", "Final fields, testable, explicit"],
        ["Services", "Concrete classes", "Interface + Impl pair per service", "Only one implementation exists (YAGNI). Spring proxies classes without interfaces"],
        ["Errors", "Exception hierarchy + `@RestControllerAdvice`", "Return codes, `ResponseStatusException`, try/catch in controllers", "Named business errors, one place that formats responses"],
        ["Page JSON", "Own `PageResponse`", "Serialising Spring's `Page`", "A stable contract that does not change with Spring internals"],
        ["Paging", "Server-side", "Load all and page in the browser", "Scales; less data sent"],
        ["Server cache", "Spring `@Cacheable`, in memory", "Redis, Caffeine", "No extra infrastructure; enough to show the concept"],
        ["CORS", "None needed (Vite proxy)", "`@CrossOrigin` / CorsConfiguration", "Same origin through the proxy; production would use a reverse proxy"],
        ["CSRF", "Disabled", "Enabled", "No cookies or sessions are used, so there is nothing for CSRF to abuse"],
        ["Concurrency control", "Transactions", "`@Version` optimistic locking", "Out of demo scope; listed as a limitation"],
        ["API docs", "README table + this guide", "springdoc / Swagger UI", "Keeps dependencies small; easy to add later"],
        ["Build", "Maven wrapper", "Gradle, system Maven", "Maven requested; wrapper pins the version"],
        ["Java version", "21 (LTS)", "17", "Current LTS with records and modern APIs; Boot 4 supports it"],
    ], [14, 22, 24, 40], small=True)
    out += h2("21.2 Frontend")
    out += table([
        ["Topic", "Used", "Not used", "Reason"],
        ["UI library", "React 19 (JSX)", "Angular, Vue; TypeScript", "Requested React with JSX; TypeScript would add compile-time types and can be introduced file by file later"],
        ["State", "Redux Toolkit", "Context + useReducer, Zustand", "Requested; DevTools support; predictable updates; Toolkit removes the old boilerplate"],
        ["HTTP", "axios", "fetch", "Requested; interceptors and automatic JSON make auth and errors simpler"],
        ["Routing", "State-based tabs", "React Router", "Only three views and no need for bookmarkable URLs; fewer dependencies. Add Router if deep links are wanted"],
        ["Build tool", "Vite", "Create React App, webpack", "Fast, current standard, built-in proxy; CRA is no longer maintained"],
        ["Tests", "Vitest + Testing Library", "Jest", "Same config as Vite, no extra transform setup"],
        ["Styling", "One plain CSS file", "Tailwind, Bootstrap, CSS-in-JS", "Small app with a custom brutalist look; no framework weight"],
        ["Token storage", "sessionStorage", "localStorage, cookie", "Disappears with the tab; an HttpOnly cookie would be safer but needs a different server design"],
        ["Data cache", "localStorage", "IndexedDB, Redux-persist", "Two small lists; a few lines of code instead of a library"],
        ["Mock backend", "Removed", "Kept alongside the real API", "Avoid two implementations drifting apart; tests mock the API module instead"],
        ["Images", "SVG pixel art", "PNG file", "No asset loading; scales crisply; stays in version control as text"],
    ], [14, 22, 24, 40], small=True)
    return out


def sample_io():
    out = h1("22. Sample input and output")
    out += p("Demo accounts: `admin / admin123`, `librarian / librarian123`, `member / member123`. The examples were produced by the running application and by the tests. "
             "Book ids depend on the seed order; ids shown are those of a fresh start.")
    out += h2("22.1 Sign in")
    out += table([
        ["Input", "Output"],
        ["`GET /api/auth/me` as librarian / librarian123", "200  `{\"username\":\"librarian\",\"role\":\"LIBRARIAN\"}`"],
        ["`GET /api/auth/me` as admin / bad", "401  `{\"message\":\"Invalid username or password.\"}`"],
        ["`GET /api/books` with no header", "401  `{\"message\":\"Authentication required.\"}`"],
    ], [42, 58])
    out += h2("22.2 Books: paging, sorting, search")
    out += code(
        "GET /api/books?query=&page=1&size=2&sort=title,desc\n"
        "200\n"
        "{\n"
        "  \"content\": [\n"
        "    {\"id\":8,\"title\":\"Spring in Action\",\"author\":\"Craig Walls\",\"isbn\":\"9781617297571\",\"available\":true,\"borrowedBy\":null},\n"
        "    {\"id\":4,\"title\":\"Refactoring\",\"author\":\"Martin Fowler\",\"isbn\":\"9780134757599\",\"available\":true,\"borrowedBy\":null}\n"
        "  ],\n"
        "  \"page\":1, \"size\":2, \"totalElements\":12, \"totalPages\":6\n"
        "}")
    out += p("`GET /api/books?query=JAVA` returns 3 books (Effective Java, Head First Java, Java Concurrency in Practice): the search ignores case and "
             "looks in title, author and ISBN. `GET /api/books?sort=nonsense,asc` returns 400 `Invalid sort or paging parameter.`")
    out += h2("22.3 Add a book")
    out += table([
        ["Input", "Output"],
        ["`POST /api/books` as librarian, body `{\"title\":\"Patterns\",\"author\":\"A. Author\",\"isbn\":\"0000000000001\"}`", "201, the new book with `\"available\":true`"],
        ["The same request again", "409 `A book with ISBN 0000000000001 already exists.`"],
        ["Body with a blank title", "400 `Title is required.`"],
        ["Same request as member", "403 `You do not have permission to do that.`"],
    ], [58, 42])
    out += h2("22.4 Issue and return")
    out += code(
        "POST /api/borrow/issue   {\"bookId\":1,\"memberId\":1}\n"
        "200\n"
        "{\"id\":1,\"title\":\"Clean Code\",\"author\":\"Robert C. Martin\",\"isbn\":\"9780132350884\",\"available\":false,\"borrowedBy\":1}\n"
        "\n"
        "POST /api/borrow/return  {\"bookId\":1}\n"
        "200\n"
        "{\"id\":1, ... \"available\":true,\"borrowedBy\":null}")
    out += table([
        ["Situation", "Status and message"],
        ["Issue a book that is already issued", "409 `\"Clean Code\" is not available.`"],
        ["Student already has 3 books and asks for a 4th", "409 `Asha Rao has reached the borrow limit of 3.`"],
        ["Return a book that is not issued", "409 `\"Clean Code\" was not issued.`"],
        ["Unknown book id", "404 `Book not found.`"],
        ["Unknown member id", "404 `Invalid member.`"],
    ], [50, 50])
    out += h2("22.5 Members")
    out += code(
        "GET /api/members?page=0&size=10&sort=type,asc    (as librarian)\n"
        "200\n"
        "{\"content\":[\n"
        "   {\"id\":2,\"name\":\"Dr. Mehta\",\"role\":\"FACULTY\",\"borrowedCount\":0},\n"
        "   {\"id\":1,\"name\":\"Asha Rao\",\"role\":\"STUDENT\",\"borrowedCount\":0}],\n"
        " \"page\":0,\"size\":10,\"totalElements\":2,\"totalPages\":1}")
    out += p("`POST /api/members` with `{\"name\":\"Ravi Kumar\",\"role\":\"STUDENT\"}` as admin returns 201; as librarian it returns 403; "
             "`GET /api/members` as member returns 403.")
    out += h2("22.6 Trying it by hand")
    out += code(
        "curl -u librarian:librarian123 \"http://localhost:8080/api/books?page=0&size=3&sort=author,asc\"\n"
        "curl -u admin:admin123 -H \"Content-Type: application/json\" ^\n"
        "     -d \"{\\\"bookId\\\":1,\\\"memberId\\\":1}\" http://localhost:8080/api/borrow/issue")
    return out


def limitations():
    out = h1("23. Known limitations and future work")
    out += p("Being clear about limits is part of a good design discussion. None of these affect the demonstrated requirements.")
    out += table([
        ["Limitation", "Why it matters", "How it could be improved"],
        ["Basic token is base64(user:password) kept in sessionStorage", "Readable by any script on the page (XSS); the password travels on every request", "HTTPS everywhere; issue short-lived tokens or HttpOnly cookies after login"],
        ["Plain HTTP in the demo", "Basic credentials are not encrypted on the wire", "Terminate TLS in a reverse proxy"],
        ["Demo passwords are written in `DataSeeder`", "Fine for a demo, unacceptable for production", "Load initial accounts from environment variables or a secret store"],
        ["No optimistic locking", "Two simultaneous requests could both issue the last available copy", "Add `@Version` to `Book` or use a pessimistic lock in `issue`"],
        ["Cache is cleared after the method returns", "In theory a read between the commit and the eviction could re-cache stale data for a moment", "Evict after commit with a transaction-synchronised cache or short expiry"],
        ["Issue / Return page loads at most 100 books and members", "Larger libraries are cut off", "Add a search-based picker or an 'available only' server filter"],
        ["Login role MEMBER is not linked to a Member record", "A MEMBER cannot see their own loans", "Add `member_id` to `AppUser` and a 'my loans' endpoint"],
        ["No edit or delete for books and members", "Mistakes cannot be corrected", "Add PUT and DELETE with rules for books currently on loan"],
        ["No due dates, fines or reservations", "Real libraries need them", "Add a Loan entity with dates; a queue for reservations"],
        ["All data lost on restart", "By design (no persistence)", "Switch the datasource to PostgreSQL and `ddl-auto=validate` with migrations"],
        ["No account lockout or rate limiting", "Password guessing is not slowed", "Spring Security lockout or a gateway rate limiter"],
        ["Member names cached in localStorage", "Visible to anyone using the same browser profile", "Cache only non-personal data, or shorten its lifetime"],
    ], [28, 34, 38], small=True)
    return out


def viva():
    out = h1("24. Likely evaluator questions, with answers")
    out += h2("Spring and Java")
    out += qa("What is IoC and where do you see it in the project?",
              "Inversion of Control means the framework creates and wires objects instead of our code. We never write `new BookService(...)`. Spring scans for `@Service`, `@RestController`, "
              "`@Component` and `@Configuration` classes, creates the beans and passes them into constructors. It also calls our code: `GlobalExceptionHandler`, "
              "`DataSeeder.run` and `DatabaseUserDetailsService` are invoked by the framework.")
    out += qa("What is dependency injection and why constructor injection?",
              "DI is how the container hands a bean the collaborators it needs. Constructor injection makes dependencies explicit and `final`, fails at startup when one is missing, and lets us test "
              "a class with plain objects or Mockito (`BorrowServiceTest`). Field injection hides dependencies and needs Spring or reflection in tests.")
    out += qa("What does @SpringBootApplication do?",
              "It combines `@SpringBootConfiguration`, `@EnableAutoConfiguration` and `@ComponentScan`: this class is a configuration source, Boot configures beans from the classpath, "
              "and Spring scans the `com.team1.library` package for components.")
    out += qa("Difference between @Component, @Service, @RestController, @Configuration?",
              "All are bean-defining stereotypes. `@Component` is generic; `@Service` marks business logic; `@RestController` marks a web endpoint whose return values become JSON; "
              "`@Configuration` holds `@Bean` methods that create beans. The specialised ones add meaning and, for controllers, web behaviour.")
    out += qa("Explain what happens when GET /api/books?query=java&page=0&size=10 arrives.",
              "Tomcat passes it through the security filter chain (Basic auth, role rule). DispatcherServlet maps it to `BookController.list`. Argument resolvers bind `query` and build a Pageable. "
              "The controller calls `BookService.search`, which is cached; on a miss the repository runs a paged, sorted query plus a count. The entities become `BookResponse` DTOs inside a `PageResponse`, "
              "which Jackson writes as JSON.")
    out += qa("What is a DTO and why use records?",
              "A Data Transfer Object defines exactly what crosses the HTTP boundary. It keeps entities (and fields like `passwordHash`) out of the API and decouples the JSON from the table design. "
              "Records are immutable and need no boilerplate.")
    out += qa("What is the N+1 problem and how did you avoid it?",
              "Loading a list and then issuing one extra query per row. For the members page we run one grouped query (`countBorrowedByMembers`) for the whole page and look counts up in a Map.")
    out += qa("What does @Transactional do?",
              "It wraps the method in a database transaction through a proxy: commit on success, roll back when a RuntimeException escapes. All business exceptions are runtime exceptions, "
              "so a failed rule undoes partial changes. Without it, the `book.issueTo` change would not be flushed because dirty checking happens at commit.")
    out += qa("Why is there no save() call in BorrowService.issue?",
              "The book is a managed entity loaded inside the transaction. Hibernate tracks changes (dirty checking) and writes the UPDATE when the transaction commits.")
    out += qa("What is the difference between @Cacheable and @CacheEvict, and what is cached?",
              "`@Cacheable` returns a stored result for the same key (query + page request) instead of running the method. `@CacheEvict(allEntries = true)` empties the cache after add, issue and return, so "
              "availability is never stale. The values are `PageResponse` DTOs.")
    out += qa("Why Spring Data JPA and what is @Entity?",
              "JPA maps Java objects to table rows; Hibernate is the implementation. `@Entity` marks a class as a table. Spring Data generates repository implementations from interfaces, "
              "including paging and sorting, so there is almost no data access code to write.")
    out += qa("How is inheritance used in the entities?",
              "`Person` is an abstract `@MappedSuperclass` with id and name. `Member` and `AppUser` extend it, so each table gets those columns. There is no separate person table.")
    out += qa("Why is AppUser separate from Member?",
              "They are different concepts: a login account with a role and password hash versus a person who borrows. A librarian can log in without borrowing; a member may have no login.")
    out += qa("Why is the database in memory and how are the demo accounts created?",
              "The requirement says not to persist data. H2 runs inside the JVM, Hibernate creates the tables at startup (`create-drop`) and `DataSeeder` inserts accounts, members and books, "
              "hashing the demo passwords with BCrypt.")
    out += qa("What are custom exceptions and how are they handled?",
              "Each business rule failure is a class extending `LibraryException` with its own HTTP status and message. `GlobalExceptionHandler` (`@RestControllerAdvice`) catches the base type "
              "polymorphically and returns `{message}` with that status. Controllers contain no try/catch.")
    out += h2("Security")
    out += qa("How does login work?",
              "The UI sends `GET /api/auth/me` with `Authorization: Basic base64(user:password)`. Spring Security decodes it, loads the user through `DatabaseUserDetailsService`, compares the password "
              "with the BCrypt hash and, if it matches, the controller returns the username and role. The UI stores the session and shows the views for that role.")
    out += qa("Is Base64 secure?",
              "No, it is only an encoding. Basic authentication must be used over HTTPS. In this demo it runs on localhost over HTTP, which is listed as a limitation.")
    out += qa("What is BCrypt and why not SHA-256?",
              "BCrypt is a slow, salted, adaptive hash designed for passwords: each hash has its own random salt and the cost can be raised over time. A fast hash like SHA-256 makes guessing cheap.")
    out += qa("Authentication vs authorization?",
              "Authentication: who are you (password check). Authorization: what may you do (role rules). 401 means not authenticated, 403 means authenticated but not allowed.")
    out += qa("How is RBAC enforced?",
              "On the server by URL rules in `SecurityConfig` with a default deny; in the UI by `permissions.js` which hides forms and tabs. The UI part is only convenience; "
              "the server always has the final say (403).")
    out += qa("Why is CSRF disabled and why STATELESS?",
              "We use no session or cookie; the credentials header is added by our own code on each request. CSRF abuses automatically attached cookies, so there is nothing to protect. "
              "Stateless means no server-side session to store or scale.")
    out += qa("Why does the 401 response have no WWW-Authenticate header?",
              "That header makes browsers open their own login prompt. Omitting it lets the React login page handle failures.")
    out += h2("Maven")
    out += qa("What is Maven and what is the pom?",
              "A build tool. `pom.xml` declares the project, its dependencies and plugins. Maven downloads libraries (including transitive ones), compiles, runs tests and packages the jar.")
    out += qa("What does mvnw do?",
              "It is the Maven Wrapper: a script that downloads and runs a pinned Maven version, so no installation is needed and all machines build identically.")
    out += qa("What is a starter and what is the parent POM?",
              "A starter is one dependency that pulls in a curated set of libraries. The parent POM manages all their versions, so they are compatible and need no version in our pom.")
    out += qa("What do spring-boot-starter-webmvc and -data-jpa give you?",
              "webmvc: Spring MVC, embedded Tomcat and Jackson for web endpoints. data-jpa: Spring Data, Hibernate, the JPA API, a connection pool and transaction management.")
    out += h2("Frontend")
    out += qa("Why Redux and how does data flow?",
              "Shared state (user, lists, banner) lives in one store. A component dispatches a thunk; the thunk calls the API; the result is dispatched as a fulfilled or rejected action; "
              "a slice reducer updates the state; components re-render through `useSelector`.")
    out += qa("What is a thunk and what does createApiThunk add?",
              "A thunk is an async action creator. `createAsyncThunk` dispatches pending, fulfilled and rejected actions automatically. Our `createApiThunk` also catches axios errors and "
              "rejects with the backend's message.")
    out += qa("What are the axios interceptors for?",
              "The request interceptor adds the Basic header from the session to every call. The response interceptor signs the user out on a 401. Both are middleware in one place instead of in every call.")
    out += qa("How do paging and sorting work end to end?",
              "The page keeps `query`, `page` and `sort` in state; a `useEffect` dispatches `fetchBooks` whenever they change. axios sends `page`, `size`, `sort`. Spring builds a Pageable and the database "
              "does the LIMIT/OFFSET and ORDER BY. The response carries totals, which drive the pager.")
    out += qa("What is the localStorage cache for?",
              "It keeps a copy of the last books and members so the page shows data immediately after a reload or when the server is down. It is cleared on sign-out and only restored while a session exists.")
    out += qa("sessionStorage vs localStorage?",
              "sessionStorage lasts for the tab; localStorage persists across restarts. We keep the login token in sessionStorage and the list cache in localStorage.")
    out += qa("What is the Vite proxy for?",
              "It forwards `/api` calls to port 8080 so the browser sees one origin; no CORS setup is needed during development.")
    out += qa("How do you test the frontend without a backend?",
              "Vitest replaces the API module with `vi.mock`, so each test controls what the API returns. The rules themselves are tested on the backend.")
    out += qa("What could you improve?",
              "HTTPS and short-lived tokens, optimistic locking for concurrent issues, edit/delete, loan history with due dates, linking a login to a member record, a real database. See chapter 23.")
    return out


def appendices():
    out = h1("Appendix A. Glossary")
    out += table([
        ["Term", "Meaning"],
        ["Annotation", "A tag such as `@Service` that gives meaning to a class or method; read by frameworks"],
        ["API / REST", "A set of URLs and JSON formats; REST uses HTTP methods (GET, POST) on resources"],
        ["Bean", "An object created and managed by the Spring container"],
        ["BOM", "Bill of materials: a list of compatible library versions"],
        ["CORS", "Browser rule restricting calls between different origins; avoided by the proxy"],
        ["CSRF", "Attack that abuses cookies attached automatically by the browser"],
        ["DTO", "Data Transfer Object: the shape of data sent or received over HTTP"],
        ["Dirty checking", "Hibernate detects changed fields of managed entities and updates them at commit"],
        ["Entity", "A class mapped to a database table"],
        ["Filter chain", "Ordered servlet filters that process each request before the controller (security lives here)"],
        ["HMR", "Hot module replacement: the dev server updates the page without a full reload"],
        ["IoC / DI", "Inversion of Control / Dependency Injection"],
        ["Immer", "Library inside Redux Toolkit that makes 'mutating' reducer code produce immutable updates"],
        ["Interceptor", "Code that runs on every axios request or response"],
        ["JPA / Hibernate", "Java persistence standard / its main implementation"],
        ["JSX", "HTML-like syntax inside JavaScript"],
        ["Middleware", "Code that sits between request and handler (axios interceptors, Redux thunk, security filters)"],
        ["ORM", "Object-relational mapping: objects to rows"],
        ["Projection", "A view of a query result with only some fields (`BorrowCount`)"],
        ["Proxy (Spring)", "A wrapper object that adds transactions or caching around a bean"],
        ["Reducer / Slice / Thunk / Selector", "See chapter 13"],
        ["SPA", "Single-page application"],
        ["Stateless", "The server stores no per-user session between requests"],
        ["Transitive dependency", "A library your library needs; Maven fetches it automatically"],
    ], [24, 76])
    out += h1("Appendix B. Commands and troubleshooting", page_break=True)
    out += table([
        ["Task", "Command"],
        ["Run backend", "`cd backend` then `mvnw.cmd spring-boot:run` (set `JAVA_HOME` to JDK 21 first)"],
        ["Run frontend", "`cd frontend`, `npm install`, `npm run dev`, open http://localhost:5173"],
        ["Backend tests", "`mvnw.cmd test`"],
        ["Build jar", "`mvnw.cmd package`, then run it with a JDK 21 `java -jar target/library-0.0.1-SNAPSHOT.jar`"],
        ["Frontend tests / lint / build", "`npm test`, `npm run lint`, `npm run build`"],
        ["Rebuild diagrams and this PDF", "`python docs/tools/diagrams.py` then `python docs/tools/build_pdf.py`"],
    ], [26, 74])
    out += table([
        ["Symptom", "Cause and fix"],
        ["`release version 21 not supported`", "`JAVA_HOME` is an older JDK. Point it to JDK 21 or newer"],
        ["`UnsupportedClassVersionError ... 61.0 ... 55.0` on `java -jar`", "The `java` on PATH is older than the jar needs. Put JDK 21 first on PATH or call its `java.exe` directly"],
        ["`PKIX path building failed` while Maven downloads", "The Maven mirror's certificate is not trusted by the JDK. Set `MAVEN_OPTS=-Djavax.net.ssl.trustStoreType=Windows-ROOT` for that terminal"],
        ["Port 8080 already in use", "Stop the other program or start with `-Dspring-boot.run.arguments=--server.port=8081` and change the proxy target"],
        ["Frontend shows a network error / 500", "The backend is not running; start it. Cached lists still display"],
        ["Login always fails", "Check the demo accounts (admin/admin123, librarian/librarian123, member/member123); data is re-seeded at each backend start"],
    ], [34, 66])
    out += h1("Appendix C. Backend source file index", page_break=True)
    out += table([
        ["File (com.team1.library)", "Purpose"],
        ["LibraryApplication", "main method; `@SpringBootApplication`"],
        ["model/Person", "Abstract base: id, name (`@MappedSuperclass`)"],
        ["model/Member, MemberType", "Borrowing person and the STUDENT/FACULTY enum with limits"],
        ["model/AppUser, Role", "Login account with password hash; ADMIN/LIBRARIAN/MEMBER"],
        ["model/Book", "Catalogue item with borrower, `issueTo`, `markReturned`, `isAvailable`"],
        ["repository/BookRepository", "Search with paging, existsByIsbn, counts"],
        ["repository/MemberRepository, AppUserRepository", "Standard JPA access; find user by username"],
        ["repository/BorrowCount", "Projection for grouped borrow counts"],
        ["dto/*", "BookRequest/Response, MemberRequest/Response, IssueRequest, ReturnRequest, UserResponse, PageResponse, ErrorResponse"],
        ["service/BookService", "Cached search, add with duplicate check"],
        ["service/MemberService", "Paged list with borrowed counts, add"],
        ["service/BorrowService", "Issue and return rules"],
        ["service/DatabaseUserDetailsService", "Loads login accounts for Spring Security"],
        ["controller/AuthController, BookController, MemberController, BorrowController", "REST endpoints"],
        ["exception/LibraryException and six subclasses", "Business errors with status and message"],
        ["exception/GlobalExceptionHandler", "Turns exceptions into JSON error responses"],
        ["config/SecurityConfig", "Basic auth, stateless, role rules, BCrypt encoder"],
        ["config/SecurityErrorHandler", "JSON 401 and 403 without WWW-Authenticate"],
        ["config/CacheConfig", "Enables caching; cache name constant"],
        ["config/DataSeeder", "Inserts demo accounts, members and books at startup"],
        ["resources/application.properties", "H2 in-memory URL, JPA mode, paging limits"],
        ["test/...", "BorrowServiceTest, LibraryApiIntegrationTest, LibraryApplicationTests"],
    ], [40, 60], small=True)
    return out
