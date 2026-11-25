import { useSelector } from 'react-redux'
import LoginPage from './features/auth/LoginPage'
import BooksPage from './features/books/BooksPage'
import BorrowPage from './features/borrow/BorrowPage'
import MembersPage from './features/members/MembersPage'
import Navbar from './features/navigation/Navbar'
import { tabsFor } from './features/navigation/tabs'
import Notice from './features/notice/Notice'

const PAGES = {
  books: BooksPage,
  members: MembersPage,
  borrow: BorrowPage,
}

export default function App() {
  const user = useSelector((state) => state.auth.user)
  const tab = useSelector((state) => state.nav.tab)

  if (!user) {
    return (
      <div className="app">
        <LoginPage />
      </div>
    )
  }

  // Fall back to the first permitted view if the stored tab is not allowed for this role.
  const allowed = tabsFor(user.role)
  const current = allowed.find((t) => t.id === tab) ?? allowed[0]
  const Page = PAGES[current.id]

  return (
    <div className="app">
      <Navbar />
      <main>
        <Notice />
        <Page />
      </main>
      <footer>Team 1 / Library Management System</footer>
    </div>
  )
}
