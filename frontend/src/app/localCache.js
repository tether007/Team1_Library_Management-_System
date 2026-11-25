// Browser-side cache: the last fetched books and members are kept in localStorage so the UI can show
// them immediately after a reload (and while the backend is unreachable). Fresh data replaces them
// as soon as the API answers. The cache is only used while a session exists and is wiped on sign-out.
import { loadSession } from '../api/authSession'

const KEY = 'lms.cache'

const isPageState = (value) => Array.isArray(value?.items) && typeof value?.pageInfo === 'object'

export const loadCache = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY))
  } catch {
    return null
  }
}

export const saveCache = (state) =>
  localStorage.setItem(KEY, JSON.stringify({ books: state.books, members: state.members }))

export const clearCache = () => localStorage.removeItem(KEY)

// State the store starts with: the signed-in user plus any cached lists.
export function restoredState() {
  const session = loadSession()
  if (!session?.user) {
    clearCache()
    return { auth: { user: null } }
  }

  const cache = loadCache()
  return {
    auth: { user: session.user },
    ...(isPageState(cache?.books) && { books: cache.books }),
    ...(isPageState(cache?.members) && { members: cache.members }),
  }
}

// Writes the cache after every store change while signed in; clears it once signed out.
export function persistOnChange(store) {
  return store.subscribe(() => {
    const state = store.getState()
    if (state.auth.user) saveCache(state)
    else clearCache()
  })
}
