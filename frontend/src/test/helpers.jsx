import { render } from '@testing-library/react'
import { Provider } from 'react-redux'
import { saveSession } from '../api/authSession'
import { createStore } from '../app/store'

// Tests replace the whole API module with vi.mock('.../api/libraryApi') and set return values per test.

export const apiError = (message) => Object.assign(new Error(message), { response: { data: { message } } })

// A backend page response.
export const pageOf = (content, extra = {}) => ({
  content,
  page: 0,
  size: 10,
  totalElements: content.length,
  totalPages: 1,
  ...extra,
})

export const book = (id, title, extra = {}) => ({
  id,
  title,
  author: 'Some Author',
  isbn: `isbn-${id}`,
  available: true,
  borrowedBy: null,
  ...extra,
})

export const member = (id, name, role = 'STUDENT', borrowedCount = 0) => ({ id, name, role, borrowedCount })

// Creates a signed-in session for a role and returns the matching preloaded state.
export function signIn(role) {
  const user = { username: role.toLowerCase(), role }
  saveSession({ token: 'dGVzdDp0ZXN0', user })
  return { auth: { user } }
}

// Store already signed in as `role` (omit for a signed-out store).
export const createStoreAs = (role) => createStore(role ? signIn(role) : undefined)

export function renderWithStore(ui, role) {
  const store = createStoreAs(role)
  return { store, ...render(<Provider store={store}>{ui}</Provider>) }
}
