from reportlab.lib.units import mm

from common import (bullets, callout, code, fig, h1, h2, h3, numbered, p, screenshot, snip, spacer, table)

F = "frontend/src/"


def overview():
    out = h1("12. Frontend overview: React, Vite and the file map")
    out += h2("12.1 What a single-page application is")
    out += p("The browser downloads **one HTML page** (`index.html`) and one JavaScript bundle. React then draws and redraws the screen by itself; "
             "switching from Books to Members does not load a new page, it only changes what React renders. Data comes from the backend "
             "as JSON through `axios`.")
    out += h2("12.2 React concepts used")
    out += table([
        ["Concept", "Meaning", "Example in the project"],
        ["Component", "A function that returns JSX (HTML-like markup). Components can contain other components", "`BooksPage`, `Navbar`, `Pager`, `Avatar`"],
        ["JSX", "Markup written inside JavaScript; Vite compiles it to plain JS", "`<button onClick={...}>Next</button>`"],
        ["Props", "Inputs passed to a component like function arguments", "`<Pager pageInfo={pageInfo} onPage={setPage} />`"],
        ["`useState`", "A value the component remembers; changing it re-renders", "search text, current page, sort order, form fields"],
        ["`useEffect`", "Run code after render, e.g. fetch data; re-runs when its dependency list changes", "`BooksPage` reloads when query, page or sort change"],
        ["`useCallback`", "Keeps the same function between renders so effects do not re-run needlessly", "`load` in `BooksPage`"],
        ["`useSelector` / `useDispatch`", "Read from the Redux store / send an action to it", "every page"],
        ["Controlled input", "The input's value comes from state and every keystroke updates the state", "all form fields"],
        ["Conditional rendering", "`{condition && <Element/>}` shows an element only when true", "Add-book form only for `books:add`"],
        ["`key` prop", "Lets React match list items between renders", "`<tr key={book.id}>`"],
        ["StrictMode", "Development helper that runs effects twice to expose bugs", "`main.jsx`"],
    ], [20, 44, 36], small=True)
    out += h2("12.3 Vite: dev server and build")
    out += bullets([
        "`npm run dev` starts the dev server on port 5173: instant start, **hot reload** (edit a file, the page updates), and the `/api` **proxy** to the backend.",
        "`npm run build` produces an optimised bundle in `dist/` (minified JavaScript and CSS) that any static web server can host.",
        "`index.html` is the entry; it contains `<div id=\"root\">` and loads `src/main.jsx`.",
        "`vite.config.js` holds the React plugin, the proxy rule and the Vitest settings (shown in chapter 14 and 19).",
    ])
    out += snip(F + "main.jsx", "import { StrictMode }", None, max_lines=25)
    out += bullets([
        "`Provider store={store}` makes the Redux store available to every component below it.",
        "`setUnauthorizedHandler(...)` registers what the HTTP layer should do on a 401: dispatch `logout`.",
        "`persistOnChange(store)` starts the localStorage cache writer (chapter 17).",
    ])
    out += h2("12.4 File map")
    out += table([
        ["File", "Purpose"],
        ["index.html, vite.config.js, eslint.config.js, package.json", "Entry page; dev/build/test config; lint rules; dependencies and scripts"],
        ["src/main.jsx", "Starts React, wires the store, 401 handler and cache"],
        ["src/App.jsx", "Chooses between login page and the signed-in layout; picks the current page by role and tab"],
        ["src/index.css", "The whole theme (colours, borders, tables, buttons)"],
        ["src/api/httpClient.js", "The axios instance and its two interceptors"],
        ["src/api/libraryApi.js", "One function per backend endpoint"],
        ["src/api/authSession.js", "Read, write and clear the login session in sessionStorage"],
        ["src/app/store.js", "`configureStore` with the five reducers; restores state at start"],
        ["src/app/createApiThunk.js", "Wrapper that turns API failures into a plain message"],
        ["src/app/localCache.js", "localStorage cache of books and members"],
        ["features/auth/", "authActions (login, logout), authSlice, permissions (RBAC), LoginPage"],
        ["features/books/", "booksActions (fetchBooks, createBook), booksSlice, BooksPage"],
        ["features/members/", "membersActions, membersSlice, MembersPage"],
        ["features/borrow/", "borrowActions (issueBook, returnBook), BorrowPage"],
        ["features/navigation/", "navSlice (active tab), tabs (which tabs a role sees), Navbar"],
        ["features/notice/", "noticeSlice (banner message), Notice component"],
        ["features/pagination/", "pageState helpers, Pager, SortHeader"],
        ["features/profile/", "Avatar: the pixel-art profile photo"],
        ["src/test/", "Vitest setup (clean storage after each test) and shared helpers"],
        ["*.test.js / *.test.jsx", "Tests, each next to the feature it checks"],
    ], [38, 62])
    return out


def redux():
    out = h1("13. State management with Redux Toolkit")
    out += h2("13.1 Why Redux, and the vocabulary")
    out += p("Several components need the same data: the navbar and every page need the current user; the borrow page needs books and members; "
             "the banner shows results of actions started elsewhere. Redux keeps that shared state in **one store** and changes it only through "
             "described events. That makes behaviour predictable and easy to test.")
    out += table([
        ["Term", "Meaning", "Example here"],
        ["Store", "The single object holding all state", "`{auth, books, members, nav, notice}`"],
        ["Action", "A plain object `{type, payload}` describing what happened", "`{type: 'books/fetch/fulfilled', payload: page}`"],
        ["Reducer", "A pure function `(state, action) -> new state`", "the rules inside `booksSlice`"],
        ["Slice", "Reducer + its action names for one feature (Redux Toolkit)", "`booksSlice.js`"],
        ["Thunk", "A function that does asynchronous work and dispatches actions as it goes", "`fetchBooks`, `login`"],
        ["Selector", "A function that reads a piece of state", "`useSelector((s) => s.books.items)`"],
        ["Dispatch", "Send an action or thunk to the store", "`dispatch(fetchBooks(params))`"],
    ], [14, 46, 40])
    out += fig("redux_flow.png", "Figure 13.1 - One-way data flow for a list request.", max_h=100 * mm)
    out += h2("13.2 The thunk helper")
    out += snip(F + "app/createApiThunk.js", "export const createApiThunk", None, max_lines=12)
    out += p("`createAsyncThunk` automatically dispatches three actions for each call: `type/pending`, `type/fulfilled` (with the result) and "
             "`type/rejected`. The wrapper catches axios errors and uses `rejectWithValue(message)` so the rejected action carries the backend's "
             "message as a simple string.")
    out += snip(F + "features/books/booksActions.js", "import", None, max_lines=6)
    out += p("An **action file** therefore contains almost no code: it names the thunk (`'books/fetch'`) and points at the API function. "
             "The same pattern is used in all features.")
    out += h2("13.3 Slices: how state changes")
    out += snip(F + "features/books/booksSlice.js", "const booksSlice", None, max_lines=22)
    out += bullets([
        "`extraReducers` reacts to actions defined **elsewhere** (thunks). `addCase(fetchBooks.fulfilled, ...)` replaces the list with the new page.",
        "`addMatcher(isAnyOf(issueBook.fulfilled, returnBook.fulfilled), ...)` handles several actions with the same code: swap the updated book into the list.",
        "Inside reducers it looks like we modify `state` directly. Redux Toolkit uses **Immer**, which turns those edits into a safe immutable update.",
        "`logout.fulfilled` resets the slice so one user's data never appears for the next.",
    ])
    out += h2("13.4 The notice slice: one place for banners")
    out += snip(F + "features/notice/noticeSlice.js", "const noticeSlice", None, max_lines=34)
    out += p("Instead of every page keeping its own error state, one slice listens to **all** rejected actions (`isRejected`) and to the four success actions. "
             "The banner therefore appears consistently for every operation, and the message text comes straight from the backend.")
    out += h2("13.5 The store")
    out += snip(F + "app/store.js", "export const createStore", None, max_lines=22)
    out += p("`createStore(preloadedState)` is a function so tests can build a fresh store each time. The exported `store` starts from `restoredState()`: "
             "the saved user and the cached lists. `configureStore` also adds the thunk middleware and the Redux DevTools hook automatically.")
    out += h2("13.6 Why features, not 'actions/ reducers/ components/' folders")
    out += p("Grouping by **feature** keeps everything that changes together in one folder. To understand or change 'borrowing' you open "
             "`features/borrow/` and find its actions, its view and its tests side by side.")
    return out


def axios_layer():
    out = h1("14. Talking to the backend: axios")
    out += snip(F + "api/httpClient.js", "// In development", None, max_lines=34)
    out += table([
        ["Piece", "What it does", "Why"],
        ["`axios.create({ baseURL: '/api' })`", "One configured client; every call is relative to `/api`", "No URL repeated in code; same origin through the proxy"],
        ["Request interceptor", "Reads the session and sets `Authorization: Basic ...` unless the call already set one", "Credentials are added in one place (a 'middleware' for outgoing requests)"],
        ["Response interceptor", "On a 401 (except from `/auth/me`) calls the registered handler, which dispatches `logout`", "Expired or invalid credentials return the user to the login page"],
        ["`setUnauthorizedHandler`", "Lets `main.jsx` provide the handler", "Avoids a circular import between the HTTP layer and the Redux store"],
        ["`errorMessage(err)`", "Picks `err.response.data.message`, else the generic error text", "Matches the backend's `{ message }` error body"],
    ], [28, 40, 32])
    out += snip(F + "api/libraryApi.js", "export const libraryApi", None, max_lines=16)
    out += p("`libraryApi` is the **only** file that knows URLs and parameter names. Thunks call these functions; components never call axios. "
             "Each function returns `response.data` (the JSON), not the whole axios response.")
    out += h2("14.1 The proxy (frontend/vite.config.js)")
    out += snip("frontend/vite.config.js", "export default defineConfig", None, max_lines=16)
    out += p("Requests from the page to `/api/...` go to the Vite server, which forwards them to `http://localhost:8080`. Browser and API share one origin, so "
             "there is no **CORS** problem and the backend needs no CORS configuration. A production deployment would put a reverse proxy "
             "(nginx, a cloud gateway) in the same place.")
    out += h2("14.2 Request and response shapes")
    out += table([
        ["Call", "axios request", "Response `data`"],
        ["login", "GET /auth/me with explicit Authorization header", "`{username, role}`"],
        ["getBooks", "GET /books, params `query, page, size, sort`", "`{content, page, size, totalElements, totalPages}`"],
        ["addBook", "POST /books, body `{title, author, isbn}`", "the new book"],
        ["getMembers", "GET /members, params `page, size, sort`", "page of members"],
        ["addMember", "POST /members, body `{name, role}`", "the new member"],
        ["issueBook", "POST /borrow/issue, body `{bookId, memberId}`", "the updated book"],
        ["returnBook", "POST /borrow/return, body `{bookId}`", "the updated book"],
    ], [18, 46, 36])
    return out


def auth_ui():
    out = h1("15. Login and role-based views in the frontend")
    out += h2("15.1 Login thunk and session")
    out += snip(F + "features/auth/authActions.js", "// Verifies", None, max_lines=16)
    out += snip(F + "api/authSession.js", "const KEY", None, max_lines=16)
    out += bullets([
        "`login` builds the token, asks the backend `GET /auth/me`, and **only on success** saves the session. A wrong password never creates a session.",
        "`sessionStorage` lives only as long as the browser tab. It survives a reload (so you stay signed in) but not closing the tab.",
        "`logout` clears the session; slices listening for `logout.fulfilled` reset themselves; the notice and nav slices reset too.",
    ])
    out += h2("15.2 Permissions and tabs")
    out += snip(F + "features/auth/permissions.js", "const ABILITIES", None, max_lines=8)
    out += snip(F + "features/navigation/tabs.js", "const TABS", None, max_lines=10)
    out += p("`can(role, ability)` is the single question every component asks. Adding a new permission means adding a string to a role's list "
             "and checking it in one component.")
    out += h2("15.3 App decides what to show")
    out += snip(F + "App.jsx", "export default function App", None, max_lines=36)
    out += bullets([
        "No user in the store -> only `LoginPage` is rendered. There is no way to reach another page.",
        "A user -> the tabs for that role; `Page` is the component of the active tab. If the stored tab is not allowed for the role, the first allowed tab is used.",
        "Inside pages, forms are hidden when `can(role, ...)` is false (for example, a MEMBER sees no 'Add book' form).",
    ])
    out += h2("15.4 Login page and navbar")
    out += snip(F + "features/auth/LoginPage.jsx", "export default function LoginPage", None, max_lines=26)
    out += snip(F + "features/navigation/Navbar.jsx", "export default function Navbar", None, max_lines=40)
    out += p("Both are plain controlled components. `Navbar` returns `null` when nobody is signed in, so it can never render with an empty user. "
             "The profile photo is the last child of the session grid, so it sits directly under the Sign out button.")
    return out


def paging_ui():
    out = h1("16. Paging, sorting and searching in the interface")
    out += p("The **server** pages and sorts; the **UI** only remembers what the user asked for and shows the result.")
    out += snip(F + "features/pagination/pageState.js", "export const PAGE_SIZE", None, max_lines=24)
    out += snip(F + "features/books/BooksPage.jsx", "export default function BooksPage", "const handleChange", max_lines=26)
    out += numbered([
        "Three pieces of local state describe the request: `query`, `page` and `sort` (`{field, dir}`).",
        "`load` is a function that dispatches `fetchBooks` with those values. `useCallback` gives it a stable identity until one of them changes.",
        "`useEffect(() => { load() }, [load])` runs `load` on first render and again whenever `query`, `page` or `sort` changes.",
        "Typing a search or clicking a header also sets `page` back to 0, so the user never lands on a page that no longer exists.",
        "The response replaces `items` and `pageInfo` in Redux, and the table and pager re-render.",
    ])
    out += snip(F + "features/pagination/Pager.jsx", "export default function Pager", None, max_lines=14)
    out += table([
        ["Sort header click", "State change", "Request sent"],
        ["First click on Title (default sort is title ascending)", "`{field: 'title', dir: 'desc'}`", "`sort=title,desc`"],
        ["Click Author", "`{field: 'author', dir: 'asc'}`", "`sort=author,asc`"],
        ["Members: click Type", "`{field: 'type', dir: 'asc'}`", "`sort=type,asc` (entity property name)"],
    ], [38, 34, 28])
    out += callout("The Issue / Return page needs every book and member for its drop-downs, so it asks for the largest page the server allows (100). "
                   "With more than 100 books or members it would show only the first 100; a search box or a server-side 'available only' filter would fix that.", "warn")
    return out


def cache_ui():
    out = h1("17. Browser cache with localStorage")
    out += p("**Idea**: remember the last lists in the browser so the screen is not empty after a reload, and so the data is still visible if the "
             "backend is temporarily unreachable. Fresh data from the server always replaces it.")
    out += snip(F + "app/localCache.js", "const KEY", None, max_lines=52)
    out += table([
        ["Function", "Role"],
        ["`restoredState()`", "At startup: if a session exists, return the user plus any cached `books` and `members` as the store's initial state; if not, delete the cache"],
        ["`persistOnChange(store)`", "Subscribes to the store. After every change: signed in -> save; signed out -> delete"],
        ["`isPageState`", "Validity check, so a corrupted or old-format cache is ignored"],
    ], [30, 70])
    out += h2("17.1 How to demonstrate it")
    out += numbered([
        "Sign in as `librarian` and open Books (the page is loaded and cached).",
        "Stop the backend.",
        "Reload the browser page. The books table still shows data from localStorage; a red banner reports that the server cannot be reached.",
        "Sign out: the cache entry is removed (browser developer tools -> Application -> Local Storage).",
    ])
    out += h2("17.2 The three storage layers compared")
    out += table([
        ["", "sessionStorage", "localStorage", "Spring cache"],
        ["Where", "Browser, per tab", "Browser, per site", "Server memory"],
        ["Holds", "Login token and user", "Last books and members lists", "Pages of books"],
        ["Cleared when", "Tab closes or sign-out", "Sign-out (or overwritten)", "A book is added, issued or returned; or restart"],
        ["Purpose", "Stay signed in after refresh", "Instant display, offline view", "Avoid repeating the same query"],
    ], [16, 28, 28, 28])
    out += callout("The cache stores member names in the browser. It is removed on sign-out and only restored while a session exists, but on a shared computer "
                   "the safest rule is still to sign out.", "warn")
    return out


def ui_theme():
    out = h1("18. Look and feel, accessibility and screens")
    out += h2("18.1 Theme")
    out += snip(F + "index.css", ":root", None, max_lines=18)
    out += bullets([
        "Style direction: **brutalist / Web 1.0**: black and white, hard 2 px borders, flat offset shadows, monospace font, no gradients or glow.",
        "Colours are CSS variables, so changing the palette is a one-line edit. Light yellow marks headers and hover; light green and red mark success and errors.",
        "A single stylesheet (`index.css`) is enough for this size; no CSS framework was added.",
    ])
    out += h2("18.2 The pixel-art profile photo")
    out += snip(F + "features/profile/Avatar.jsx", "const PIXELS", None, max_lines=34)
    out += p("The picture is an 8 by 8 grid written as text. Each character becomes one SVG square, so there is **no image file** and the art stays sharp at any size. "
             "It sits in a CSS grid under the Sign out button and stretches to the button's width. Later a real uploaded photo can replace it through the same component.")
    out += h2("18.3 Accessibility")
    out += bullets([
        "Every input has a label or `aria-label`; the profile photo has `role=\"img\"` and a text description.",
        "Errors use `role=\"alert\"`, successes `role=\"status\"`, so screen readers announce them.",
        "Sortable column headers expose `aria-sort`; the current tab has `aria-current=\"page\"`.",
        "Focus outlines are strong (3 px) and buttons can be used with the keyboard.",
    ])
    out += h2("18.4 Screens")
    out += p("Paste the screenshots of the running application into the frames below (the file names show where automatic screenshots would go).")
    out += screenshot("ui_login.png", "Figure 18.1 - Sign-in page with the three demo accounts listed under the form.")
    out += screenshot("ui_books_librarian.png", "Figure 18.2 - Books page as librarian: add form, search, sortable headers, status badges, pager.")
    out += screenshot("ui_issue.png", "Figure 18.3 - Issue / Return page: choose an available book and a member; issued books listed with Return buttons.")
    out += screenshot("ui_members_admin.png", "Figure 18.4 - Members page as admin: add-member form, type and borrowed count, pager.")
    out += screenshot("ui_member_view.png", "Figure 18.5 - Member role: only the Books tab and no add form.")
    out += screenshot("ui_error.png", "Figure 18.6 - Red banner after an invalid operation (for example issuing a book that is already issued).")
    return out
