from reportlab.lib.units import mm
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle

from common import (BLACK, CONTENT_W, YELLOW, bullets, callout, fig, fmt, h1, h2, h3, make_toc, numbered, p, screenshot, spacer, table)
from reportlab.lib.styles import ParagraphStyle


def cover():
    t1 = ParagraphStyle("CoverTitle", fontName="Helvetica-Bold", fontSize=30, leading=36)
    t2 = ParagraphStyle("CoverSub", fontName="Helvetica", fontSize=14, leading=19)
    t3 = ParagraphStyle("CoverSmall", fontName="Helvetica", fontSize=10, leading=14)
    box = Table([[Paragraph("LIBRARY<br/>MANAGEMENT<br/>SYSTEM", t1)]], colWidths=[CONTENT_W * 0.92])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 2.5, BLACK), ("BACKGROUND", (0, 0), (-1, -1), YELLOW),
                             ("LEFTPADDING", (0, 0), (-1, -1), 16), ("TOPPADDING", (0, 0), (-1, -1), 18),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 18)]))
    meta = [["Spring Boot 4.2 + React 19", "Java 21, Maven, Redux Toolkit, axios, Vitest, JUnit 5"]]
    return [Spacer(1, 40 * mm), box, Spacer(1, 10 * mm),
            Paragraph("Project Guide and Evaluation Companion", t2), Spacer(1, 4 * mm),
            Paragraph("Requirements, architecture, every library, every Spring annotation, a walk-through of the "
                      "backend and frontend code, request traces, tests, design decisions and likely viva questions.", t3),
            Spacer(1, 14 * mm),
            Paragraph("Team 1 - Library Management System (CAIT-LMS)", t3),
            Paragraph("Backend: Spring Boot 4.2.0, Java 21, Maven wrapper", t3),
            Paragraph("Frontend: React 19, Vite, Redux Toolkit, axios, Vitest", t3),
            NextPageTemplate("rest"), PageBreak()]


def how_to_read():
    out = [Paragraph("Contents", ParagraphStyle("TocTitle", fontName="Helvetica-Bold", fontSize=19, leading=23, spaceAfter=10))]
    out.append(make_toc())
    out += h1("How to use this guide")
    out += p("This guide is written so that you can **explain the project to an evaluator** without reading every source file first. "
             "Each chapter answers three questions: **what** the piece is, **why** it was chosen (and what was deliberately not used), "
             "and **where** in the code it lives.")
    out += table([
        ["If the evaluator asks about...", "Go to chapter"],
        ["What the system must do, who uses it", "2 Requirements"],
        ["How the whole system fits together", "3 Architecture"],
        ["A library or tool (Spring Boot starters, Maven, React, Redux, axios, Vitest...)", "4 Libraries, 5 Maven, 6 Spring concepts"],
        ["DI, IoC, annotations, entities, transactions, caching", "6 Spring concepts, 7 Backend walk-through"],
        ["What a URL mapping does and what it calls", "8 API reference and request traces"],
        ["Login, roles, passwords", "9 Security"],
        ["Errors and custom exceptions", "10 Exception handling"],
        ["Why a given Java collection", "11 Collections"],
        ["React, Redux, axios, localStorage, paging", "12 to 18 Frontend"],
        ["Tests", "19 Testing"],
        ["OOP principles and design choices", "20 OOP mapping, 21 Decision log"],
        ["Sample inputs and outputs", "22 Sample input/output"],
        ["Weak points and future work", "23 Limitations"],
        ["Quick practice questions", "24 Viva Q&A"],
    ], [58, 42])
    out += callout("Everything in the code excerpts is copied from the real source files by the script that builds this PDF "
                   "(docs/tools/build_pdf.py), so the excerpts always match the repository.", "info")
    return out


def overview():
    out = h1("1. Project overview")
    out += h2("1.1 The problem")
    out += p("A library needs to keep a catalogue of books and a list of members, let staff lend books to members and take them back, "
             "and show at any time which books are available. Doing this on paper or in a spreadsheet leads to double-lending, "
             "forgotten returns and no limit on how many books one person holds. This project is a small web application that "
             "enforces those rules automatically.")
    out += h2("1.2 What was built")
    out += bullets([
        "A **REST backend** (Spring Boot) that owns the data and every business rule.",
        "A **single-page frontend** (React) that talks to the backend through JSON over HTTP.",
        "**Login** with username and password, checked against a database table, and **role-based views** for administrators, librarians and members.",
        "**Paging, sorting and searching** of books and members, done by the server.",
        "**Custom exceptions** for every invalid operation (book not available, borrow limit reached, unknown member, ...).",
        "Two kinds of caching to show the idea: a **server-side cache** (Spring Cache) and a **browser cache** (localStorage).",
        "Automated tests: **23 JUnit tests** on the backend and **42 Vitest tests** on the frontend.",
    ])
    out += h2("1.3 Technology at a glance")
    out += table([
        ["Layer", "Technology", "Version in this project"],
        ["Language (backend)", "Java", "21 (LTS)"],
        ["Framework (backend)", "Spring Boot (Spring Framework 7, Spring Security 7, Spring Data JPA, Hibernate)", "4.2.0"],
        ["Build tool", "Apache Maven through the Maven Wrapper (mvnw)", "wrapper downloads Maven"],
        ["Database", "H2, in-memory, not persisted", "managed by Boot BOM"],
        ["Backend tests", "JUnit 5, Mockito, AssertJ, Spring MockMvc, Spring Security Test", "from the test starters"],
        ["Frontend runtime", "React and React DOM", "19.3.1"],
        ["Frontend build / dev server", "Vite with @vitejs/plugin-react", "8.3.6"],
        ["State management", "Redux Toolkit and react-redux", "2.14 / 9.3"],
        ["HTTP client", "axios", "1.21"],
        ["Frontend tests", "Vitest, jsdom, React Testing Library, user-event, jest-dom", "5.1 / 31 / 16.3 / 14.6 / 7.0"],
        ["Code quality", "ESLint with react-hooks and react-refresh plugins", "10.14"],
    ], [24, 52, 24])
    out += h2("1.4 Repository layout")
    out += p("The two applications live in separate folders and share nothing except the REST contract.")
    from common import code
    out += code(
        "Team1_Library_Management-_System/\n"
        "  README.md              run instructions, API table, principles table\n"
        "  CHANGELOG.md           running log of every change\n"
        "  docs/                  this guide, design diagrams, images, generator scripts\n"
        "  backend/               Spring Boot (Maven)\n"
        "    pom.xml  mvnw  mvnw.cmd  .mvn/\n"
        "    src/main/java/com/team1/library/\n"
        "        LibraryApplication.java\n"
        "        model/ repository/ service/ controller/ dto/ exception/ config/\n"
        "    src/main/resources/application.properties\n"
        "    src/test/java/com/team1/library/   (JUnit tests)\n"
        "  frontend/              React (Vite)\n"
        "    package.json  vite.config.js  eslint.config.js  index.html\n"
        "    src/api/  src/app/  src/features/  src/test/\n"
        "    src/App.jsx  src/main.jsx  src/index.css")
    return out


def requirements():
    out = h1("2. Requirements")
    out += p("Requirements say **what** the system must do (functional) and **how well** it must do it (non-functional). "
             "Each functional requirement below is traced to the code that satisfies it and the test that checks it.")
    out += h2("2.1 Actors (users)")
    out += table([
        ["Actor", "Who they are", "What they may do"],
        ["ADMIN", "System administrator", "Everything: view and search books, add books, list members, add members, issue and return books"],
        ["LIBRARIAN", "Library staff", "View and search books, add books, list members, issue and return books (cannot add members)"],
        ["MEMBER", "Reader with a login", "View and search books only"],
    ], [18, 28, 54])
    out += callout("Do not confuse the two meanings of 'member'. A **Member** record (STUDENT or FACULTY) is a person who borrows books. "
                   "The **MEMBER login role** is the lowest permission level of someone who signs in. They are separate on purpose "
                   "(see limitations).", "info")
    out += h2("2.2 Functional requirements")
    out += table([
        ["ID", "Requirement", "Implemented in", "Checked by"],
        ["FR1", "A user signs in with username and password verified against a database table", "SecurityConfig, DatabaseUserDetailsService, AppUser; frontend authActions.login", "LibraryApiIntegrationTest (3 auth tests); auth.test.jsx"],
        ["FR2", "Three roles with different permissions (RBAC)", "SecurityConfig URL rules; permissions.js", "memberCannotAddBooksOrIssueThem, onlyAdminCanAddMembers..."],
        ["FR3", "View and search books by title, author or ISBN, case-insensitive", "BookService.search, BookRepository derived query", "searchMatchesTitleAuthorOrIsbnIgnoringCase"],
        ["FR4", "Page and sort books and members", "Pageable in controllers; Pager and SortHeader in the UI", "booksAreSortedByTitleAndPagedByDefault, clientControlsPageSize..."],
        ["FR5", "Add a book; ISBN must be unique, fields required", "BookService.add, BookRequest validation, DuplicateIsbnException", "librarianAddsABookAndDuplicateIsbnIsRejected"],
        ["FR6", "Add a member (student or faculty); admin only", "MemberService.add, MemberController", "onlyAdminCanAddMembers..."],
        ["FR7", "List members with the number of books each holds", "MemberService.list, BookRepository.countBorrowedByMembers", "issueAndReturnUpdateAvailabilityAndBorrowedCount"],
        ["FR8", "Issue a book to a member: book must be available, member under the limit (student 3, faculty 5)", "BorrowService.issue", "BorrowServiceTest (5 tests), studentCannotBorrowMoreThanThreeBooks"],
        ["FR9", "Return an issued book", "BorrowService.giveBack", "issueAndReturn..., giveBackRejectsBookThatWasNotIssued"],
        ["FR10", "Show the availability of every book", "Book.isAvailable, BookResponse.available, status badge in BooksPage", "issueAndReturn..."],
        ["FR11", "Every invalid operation returns a clear message", "LibraryException subclasses, GlobalExceptionHandler, SecurityErrorHandler", "all 409 / 404 / 403 / 401 assertions"],
        ["FR12", "Sign out; staying signed in after a page refresh", "authActions.logout, authSession (sessionStorage)", "auth.test.jsx, App.test.jsx"],
        ["FR13", "Each role sees only the views and forms it may use", "tabs.js, permissions.js, BooksPage, MembersPage", "navigation.test.jsx, books.test.jsx, members.test.jsx"],
        ["FR14", "A default pixel-art profile photo under the Sign out button", "features/profile/Avatar.jsx, Navbar.jsx", "avatar.test.jsx, navigation.test.jsx"],
        ["FR15", "Demo data (accounts, members, books) available at start", "DataSeeder", "all integration tests rely on it"],
    ], [7, 34, 33, 26], small=True)
    out += h2("2.3 Non-functional requirements")
    out += table([
        ["ID", "Category", "Requirement", "How it is met"],
        ["NFR1", "Security", "Passwords never stored in plain text; every request authenticated; permissions enforced on the server", "BCrypt hashes, HTTP Basic on every call, URL rules in SecurityConfig, stateless (no session cookie)"],
        ["NFR2", "Performance", "Lists must not load the whole table", "Database-level paging and sorting (LIMIT/OFFSET, ORDER BY); page size capped at 100; repeated searches served by @Cacheable"],
        ["NFR3", "Reliability", "A failed operation must not leave half-done changes", "@Transactional services; validation before work; unique constraint on ISBN"],
        ["NFR4", "Usability", "Clear feedback, consistent look, keyboard and screen-reader friendly", "Success and error banners (role alert / status), labelled inputs (aria-label), aria-sort on sortable headers, simple black-and-white theme"],
        ["NFR5", "Maintainability", "Easy to find and change code", "Layered backend (controller -> service -> repository); frontend grouped by feature; one responsibility per class; comments marking IoC/DI"],
        ["NFR6", "Testability", "Business rules testable without a server", "Constructor injection allows Mockito tests; MockMvc tests the full stack in-process; 65 automated tests"],
        ["NFR7", "Portability", "Runs on a developer laptop with no installation of a database", "In-memory H2; Maven wrapper; Node LTS only"],
        ["NFR8", "Data policy", "Data must not be persisted (assignment decision)", "H2 mem database recreated at each start; browser caches are only copies and are cleared on sign-out"],
        ["NFR9", "Compatibility", "Works in current desktop browsers", "Standard React 19 / ES modules, no browser-specific features"],
        ["NFR10", "Documentation", "Another developer can run and understand the project", "README, CHANGELOG, this guide, comments, design diagrams"],
    ], [7, 14, 34, 45], small=True)
    out += h2("2.4 Business rules")
    out += numbered([
        "A book can be issued only if it has no borrower (it is **available**).",
        "A **student** may hold at most **3** books; **faculty** at most **5**.",
        "A book can be returned only if it is currently **issued**.",
        "Two books may not share an **ISBN**.",
        "Title, author and ISBN are required when adding a book; name and member type are required when adding a member.",
        "Only ADMIN and LIBRARIAN may issue and return; only ADMIN may add members.",
    ])
    out += h2("2.5 Constraints, assumptions and scope")
    out += bullets([
        "**No persistent database**: data lives in memory and is recreated at startup (assignment requirement).",
        "**Java 21** and **Spring Boot 4** are used because they are the current releases at the time of writing.",
        "One library branch, one copy per book (no copy counts), no due dates or fines.",
        "**Out of scope**: editing or deleting books and members, reservations, email notices, password change, user management screens, payments.",
    ])
    return out


def architecture():
    out = h1("3. Architecture")
    out += h2("3.1 Big picture")
    out += p("The browser runs the React application. During development the Vite dev server serves the page on port 5173 and "
             "**forwards every URL that starts with `/api`** to the Spring Boot application on port 8080 (the 'proxy'). "
             "Because the browser thinks it is talking to one origin, no CORS configuration is needed.")
    out += fig("architecture.png", "Figure 3.1 - System architecture. Left: the browser. Right: the Spring Boot application with its layers.")
    out += h2("3.2 Backend layers and what each is allowed to do")
    out += table([
        ["Layer", "Package", "Job", "Must NOT"],
        ["Controller", "controller", "Map an HTTP request to a Java method, validate input, return a DTO", "Contain business rules or touch the database"],
        ["Service", "service", "Business rules, transactions, caching", "Know about HTTP, JSON or status codes"],
        ["Repository", "repository", "Read and write entities with Spring Data JPA", "Contain business rules"],
        ["Model", "model", "Entities (rows) and enums, with small behaviours like issueTo()", "Depend on Spring web classes"],
        ["DTO", "dto", "The exact shapes of request and response JSON (Java records)", "Carry behaviour"],
        ["Exception", "exception", "Business error types and one central handler", "Be caught in controllers"],
        ["Config", "config", "Security rules, caching switch, demo data", "Hold business logic"],
    ], [14, 14, 40, 32])
    out += p("Why layers? Each layer has one reason to change. A change in the JSON format touches DTOs and controllers only; "
             "a change in the lending rule touches `BorrowService` only; a change of database touches configuration only.")
    out += h2("3.3 Frontend layers")
    out += table([
        ["Part", "Folder", "Job"],
        ["Views", "features/*/XxxPage.jsx", "React components that show data and collect input"],
        ["Actions", "features/*/xxxActions.js", "Redux thunks: functions that call the API and describe the outcome as actions"],
        ["Slices", "features/*/xxxSlice.js", "Reducers: how state changes in response to actions"],
        ["API", "api/", "axios client, interceptors, one function per endpoint, session storage helper"],
        ["App wiring", "app/", "The Redux store, the localStorage cache, the thunk helper"],
    ], [18, 32, 50])
    out += h2("3.4 Where data lives")
    out += table([
        ["Place", "What is kept", "Lifetime"],
        ["H2 in-memory database (server)", "Accounts, members, books and who borrowed what", "Until the backend stops"],
        ["Spring cache 'books' (server memory)", "Recently requested pages of books", "Until a write clears it or the backend stops"],
        ["Redux store (browser memory)", "Current user, current page of books and members, banner message, active tab", "Until the page is reloaded"],
        ["sessionStorage 'lms.session' (browser)", "The signed-in user and the Basic-auth token", "Until the tab is closed or the user signs out"],
        ["localStorage 'lms.cache' (browser)", "A copy of the last books and members lists", "Until sign-out (removed) or overwritten by fresh data"],
    ], [34, 44, 22])
    out += h2("3.5 Startup sequence of the backend")
    out += numbered([
        "`mvnw spring-boot:run` compiles the code and runs `LibraryApplication.main`.",
        "`SpringApplication.run` creates the **ApplicationContext** (the IoC container).",
        "**Component scan** finds every class annotated `@Service`, `@RestController`, `@Component`, `@Configuration` under `com.team1.library`.",
        "**Auto-configuration** reacts to what is on the classpath: H2 present -> a DataSource is created from `spring.datasource.url`; "
        "JPA present -> Hibernate builds an EntityManagerFactory and, because `ddl-auto=create-drop`, creates the tables from the @Entity classes; "
        "Spring Data creates an implementation for every repository interface; caching and security are switched on.",
        "The container creates the beans in dependency order and passes each one into the constructors that need it (**dependency injection**).",
        "An embedded **Tomcat** starts on port 8080 and registers the Spring Security filter chain and the DispatcherServlet.",
        "`DataSeeder` (an `ApplicationRunner`) inserts the demo accounts, members and books.",
        "The application is ready to accept requests.",
    ])
    return out
