import { render } from '@testing-library/react'
import { Provider } from 'react-redux'
import { encodeBasicToken, saveSession } from '../api/authSession'
import { MOCK_USERS } from '../api/mockAdapter'
import { createStore } from '../app/store'

// Creates a signed-in session for a demo role and returns the matching preloaded state.
export function signIn(role) {
  const { username, password } = MOCK_USERS.find((u) => u.role === role)
  const user = { username, role }
  saveSession({ token: encodeBasicToken(username, password), user })
  return { auth: { user } }
}

// Store already signed in as `role` (omit for a signed-out store).
export const createStoreAs = (role) => createStore(role ? signIn(role) : undefined)

export function renderWithStore(ui, role) {
  const store = createStoreAs(role)
  return { store, ...render(<Provider store={store}>{ui}</Provider>) }
}
