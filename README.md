# Library Management System

A library application with a Spring Boot REST backend and a React frontend. It manages books, members, borrowing, returning and book availability, with login and role-based views.

## Repository Structure

```
Team1_Library_Management-_System/
├── README.md
├── CHANGELOG.md                 # Running log of changes
├── docs/
│   └── design-diagram.md        # Class and activity diagrams (Mermaid)
├── backend/                     # Spring Boot 4 (Java 21, Maven)
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/team1/library/
│       │   ├── LibraryApplication.java
│       │   ├── model/           # JPA entities: Person (abstract) -> Member, AppUser; Book; enums
│       │   ├── repository/      # Spring Data repositories
│       │   ├── service/         # Business rules (BookService, MemberService, BorrowService, user lookup)
│       │   ├── controller/      # REST controllers
│       │   ├── dto/             # Request / response records, PageResponse
│       │   ├── exception/       # Custom exceptions + global handler
│       │   └── config/          # Security, cache, demo data seeding
│       ├── main/resources/application.properties
│       └── test/java/com/team1/library/   # JUnit 5 tests
└── frontend/                    # React 19 (Vite, JSX)
    └── src/
        ├── api/                 # axios client + interceptors, API functions, session storage
        ├── app/                 # Redux store, localStorage cache, createApiThunk
        ├── features/
        │   ├── auth/            # authActions, authSlice, permissions (RBAC), LoginPage, tests
        │   ├── books/           # booksActions, booksSlice, BooksPage, tests
        │   ├── members/         # membersActions, membersSlice, MembersPage, tests
        │   ├── borrow/          # borrowActions, BorrowPage, tests
        │   ├── pagination/      # Pager, SortHeader, paging/sorting helpers, tests
        │   ├── navigation/      # navSlice, tabs, Navbar, tests
        │   ├── profile/         # Avatar (default pixel-art profile photo), tests
        │   └── notice/          # noticeSlice, Notice banner
        └── test/                # shared test setup and helpers
```

## Running the Project

Prerequisites: JDK 21 or newer and Node.js (LTS). Maven is not needed separately; the backend ships the Maven wrapper (`mvnw` / `mvnw.cmd`). Check your Java version with `java -version`; JDK 11 or 17 will not build this project.

### 1. Backend (http://localhost:8080)

PowerShell on Windows:

```powershell
cd backend

# Point this terminal at JDK 21 (adjust the path to where your JDK 21 is installed)
$env:JAVA_HOME = "C:\path\to\jdk-21"

# Only if the build fails with a certificate (PKIX) error behind a corporate proxy or Maven mirror:
$env:MAVEN_OPTS = "-Djavax.net.ssl.trustStoreType=Windows-ROOT"

.\mvnw.cmd spring-boot:run
```

macOS / Linux:

```bash
cd backend
export JAVA_HOME=/path/to/jdk-21
./mvnw spring-boot:run
```

- The first run downloads Maven and all dependencies, so it takes a few minutes.
- The backend is ready when the log shows Tomcat started on port 8080.
- Quick check: `curl -u admin:admin123 http://localhost:8080/api/auth/me` returns `{"username":"admin","role":"ADMIN"}`.
- Stop it with Ctrl+C. The in-memory data is discarded and reseeded on the next start.
- `JAVA_HOME` and `MAVEN_OPTS` last only for the terminal window. To keep JDK 21 permanently, install it system-wide or set `JAVA_HOME` in your user environment variables.

### 2. Frontend (http://localhost:5173)

In a second terminal, with the backend running:

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://localhost:8080`. On Windows PowerShell use `npm.cmd` if `npm` is blocked by the execution policy.

### 3. Sign in

Demo accounts (seeded at startup): `admin / admin123`, `librarian / librarian123`, `member / member123`.

### Tests and builds

```bash
# Backend (from backend/; use mvnw.cmd on Windows)
./mvnw test        # JUnit 5: 23 tests (unit + full-stack MockMvc)
./mvnw package     # runs the tests, then builds target/library-0.0.1-SNAPSHOT.jar
java -jar target/library-0.0.1-SNAPSHOT.jar   # runs the packaged jar; `java` must be JDK 21+ (see below)

# Frontend (from frontend/)
npm test           # Vitest, single run
npm run lint
npm run build      # production bundle in dist/
```

### Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `release version 21 not supported` or `invalid target release` | `JAVA_HOME` points to an older JDK. Set it to JDK 21 or newer. |
| `UnsupportedClassVersionError ... class file version 61.0 ... up to 55.0` when running `java -jar` | The `java` on your PATH is older than the jar needs. `JAVA_HOME` only affects Maven, not `java`. Put JDK 21 first on the PATH (`$env:Path = "$env:JAVA_HOME\bin;$env:Path"`) or call `"$env:JAVA_HOME\bin\java.exe" -jar ...`. |
| `PKIX path building failed` during dependency download | The Maven mirror uses a certificate your JDK does not trust. Set `MAVEN_OPTS` as shown above, or add the certificate to the JDK trust store. |
| Port 8080 already in use | Stop the other process, or start the backend with `.\mvnw.cmd spring-boot:run "-Dspring-boot.run.arguments=--server.port=8081"` and change the proxy target in `frontend/vite.config.js`. |
| Frontend shows `Request failed with status code 500` or a network error | The backend is not running. Start it first. Cached books and members from the last session still display. |

## Data Storage

- **No persistent database.** The backend uses an in-memory H2 database (`jdbc:h2:mem`). It is created and seeded at startup (3 accounts, 2 members, 12 books) and discarded on shutdown.
- **Server cache.** `BookService.search` is cached with Spring's `@Cacheable` (in-memory). Adding a book, issuing or returning clears it.
- **Browser cache.** The frontend keeps the last fetched books and members in `localStorage` (`lms.cache`) and shows them straight after a reload, then replaces them with fresh data. To see it: sign in, open the Books tab, stop the backend and reload the page; the list still appears with an error banner. The cache is used only while a session exists and is removed on sign-out. The login session itself (Basic token) is in `sessionStorage`.

## API

Base path `/api`. Every request carries `Authorization: Basic base64(username:password)`. Spring Security checks it against the `app_users` table (BCrypt hashes).
Errors return `{ "message": "..." }` with status 400 (invalid input or sort), 401 (bad or missing credentials), 403 (role not allowed), 404 (not found), or 409 (rule violation). The 401 response has no `WWW-Authenticate` header, so browsers do not open their own login dialog.

| Method | Path | Roles | Body / params | Returns |
|---|---|---|---|---|
| GET | `/auth/me` | any | | `{ username, role }` |
| GET | `/books` | any | `query`, `page`, `size`, `sort` | page of `Book` |
| POST | `/books` | ADMIN, LIBRARIAN | `{ title, author, isbn }` | `Book` (201; 409 on duplicate ISBN) |
| GET | `/members` | ADMIN, LIBRARIAN | `page`, `size`, `sort` | page of `Member` |
| POST | `/members` | ADMIN | `{ name, role }` (`STUDENT` or `FACULTY`) | `Member` (201) |
| POST | `/borrow/issue` | ADMIN, LIBRARIAN | `{ bookId, memberId }` | `Book` (409 if unavailable or over the limit: student 3, faculty 5) |
| POST | `/borrow/return` | ADMIN, LIBRARIAN | `{ bookId }` | `Book` (409 if not issued) |

- **Paging and sorting:** `page` starts at 0; `size` defaults to 10 and is capped at 100; `sort` is `field,asc|desc`. Sortable fields are entity properties: books `id, title, author, isbn`; members `id, name, type` (`type` is returned as `role`). Unknown fields return 400.
- **Page shape:** `{ content, page, size, totalElements, totalPages }`.
- **Shapes:** `Book` = `{ id, title, author, isbn, available, borrowedBy }`. `Member` = `{ id, name, role, borrowedCount }`.
- **Login roles:** `ADMIN` (everything), `LIBRARIAN` (add books, view members, issue and return), `MEMBER` (view and search books).

## Where the Spring and OOP Principles Are Used

Each place is also marked with a comment in the code.

| Principle | Where |
|---|---|
| Inversion of Control | `LibraryApplication` (`@SpringBootApplication` component scan); `@Configuration`/`@Bean` in `SecurityConfig`; `@RestControllerAdvice` in `GlobalExceptionHandler` and the `UserDetailsService` bean found by Spring Security |
| Dependency Injection (constructor) | `BookController`, `BookService`, `BorrowService`, `MemberService`, `DataSeeder`, `DatabaseUserDetailsService`; `SecurityConfig.securityFilterChain` receives `SecurityErrorHandler` |
| Spring-managed components | `@Service`, `@RestController`, `@Component` (`SecurityErrorHandler`, `DataSeeder`), `@Configuration`, Spring Data repository interfaces |
| `@Entity` | `Book`, `Member`, `AppUser` (`Person` is a `@MappedSuperclass`) |
| Inheritance, abstraction | `Person` (abstract) -> `Member`, `AppUser`; `LibraryException` (abstract) -> six concrete exceptions |
| Polymorphism | `GlobalExceptionHandler` handles any `LibraryException`; each subclass supplies its own status and message |
| Encapsulation | `Book` changes availability only through `issueTo` / `markReturned`; availability is derived from the borrower |
| Interfaces | Repository interfaces, `BorrowCount` projection, `UserDetailsService`, `AuthenticationEntryPoint` / `AccessDeniedHandler` |
| Exception handling | `exception/` package; every rule violation maps to a status and message |
| AOP-style annotations | `@Transactional`, `@Cacheable`, `@CacheEvict` |

Not built yet: method overloading and a hand-written use of `Collection` types such as `Queue` or `Set`. Only `List` and `Map` appear in `MemberService`.

## Conventions

- Backend and frontend stay in separate folders and communicate only through the REST API.
- Every change is recorded in `CHANGELOG.md`.
- Frontend code is grouped by feature (actions, slice, view and tests together).
