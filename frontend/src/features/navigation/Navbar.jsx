import { useDispatch, useSelector } from 'react-redux'
import { logout } from '../auth/authActions'
import { setTab } from './navSlice'
import { tabsFor } from './tabs'

export default function Navbar() {
  const dispatch = useDispatch()
  const user = useSelector((state) => state.auth.user)
  const active = useSelector((state) => state.nav.tab)

  if (!user) return null

  return (
    <header className="navbar">
      <div className="navbar-top">
        <h1>LIBRARY MANAGEMENT SYSTEM</h1>
        <div className="session">
          <span>{user.username} [{user.role}]</span>
          <button onClick={() => dispatch(logout())}>Sign out</button>
        </div>
      </div>
      <nav>
        {tabsFor(user.role).map((tab) => (
          <button
            key={tab.id}
            className={tab.id === active ? 'tab active' : 'tab'}
            aria-current={tab.id === active ? 'page' : undefined}
            onClick={() => dispatch(setTab(tab.id))}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </header>
  )
}
