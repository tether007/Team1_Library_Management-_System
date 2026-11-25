import { useState } from 'react'
import { useDispatch } from 'react-redux'
import Notice from '../notice/Notice'
import { login } from './authActions'

export default function LoginPage() {
  const dispatch = useDispatch()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    dispatch(login({ username, password }))
  }

  return (
    <main className="login">
      <h2>Sign in</h2>
      <Notice />

      <form className="stack" onSubmit={handleSubmit}>
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        <button type="submit">Sign in</button>
      </form>

      <p className="hint">
        Demo accounts: admin / admin123, librarian / librarian123, member / member123
      </p>
    </main>
  )
}
