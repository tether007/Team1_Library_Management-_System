import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { loadSession } from '../../api/authSession'
import { createStoreAs, renderWithStore } from '../../test/helpers'
import { login, logout } from './authActions'
import LoginPage from './LoginPage'
import { can } from './permissions'

describe('auth actions', () => {
  it('signs in with valid credentials and keeps the session', async () => {
    const store = createStoreAs()
    await store.dispatch(login({ username: 'librarian', password: 'librarian123' }))

    expect(store.getState().auth.user).toEqual({ username: 'librarian', role: 'LIBRARIAN' })
    expect(loadSession().user.role).toBe('LIBRARIAN')
  })

  it('rejects a wrong password', async () => {
    const store = createStoreAs()
    await store.dispatch(login({ username: 'admin', password: 'nope' }))

    expect(store.getState().auth.user).toBeNull()
    expect(store.getState().notice.message).toEqual({ type: 'error', text: 'Invalid username or password.' })
    expect(loadSession()).toBeNull()
  })

  it('signs out and clears the session', async () => {
    const store = createStoreAs('ADMIN')
    await store.dispatch(logout())

    expect(store.getState().auth.user).toBeNull()
    expect(loadSession()).toBeNull()
  })
})

describe('permissions', () => {
  it('gives each role its own abilities', () => {
    expect(can('ADMIN', 'members:add')).toBe(true)
    expect(can('LIBRARIAN', 'members:add')).toBe(false)
    expect(can('LIBRARIAN', 'borrow:manage')).toBe(true)
    expect(can('MEMBER', 'borrow:manage')).toBe(false)
    expect(can('UNKNOWN', 'books:view')).toBe(false)
  })
})

describe('LoginPage', () => {
  it('shows the backend error for bad credentials', async () => {
    const user = userEvent.setup()
    renderWithStore(<LoginPage />)

    await user.type(screen.getByLabelText('Username'), 'admin')
    await user.type(screen.getByLabelText('Password'), 'wrong')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid username or password.')
  })
})
