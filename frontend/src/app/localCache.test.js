import { describe, expect, it } from 'vitest'
import { saveSession } from '../api/authSession'
import { signIn } from '../test/helpers.jsx'
import { clearCache, loadCache, persistOnChange, restoredState, saveCache } from './localCache'
import { createStore } from './store'

const cachedBooks = {
  items: [{ id: 1, title: 'Clean Code' }],
  pageInfo: { page: 0, size: 10, totalElements: 1, totalPages: 1 },
}

describe('localStorage cache', () => {
  it('restores cached lists for a signed-in session', () => {
    const { auth } = signIn('LIBRARIAN')
    saveCache({ books: cachedBooks, members: { items: [], pageInfo: {} } })

    const state = restoredState()

    expect(state.auth).toEqual(auth)
    expect(state.books).toEqual(cachedBooks)
  })

  it('ignores and wipes the cache when nobody is signed in', () => {
    saveCache({ books: cachedBooks, members: cachedBooks })

    expect(restoredState()).toEqual({ auth: { user: null } })
    expect(loadCache()).toBeNull()
  })

  it('ignores a cache with an unexpected shape', () => {
    saveSession({ token: 't', user: { username: 'a', role: 'ADMIN' } })
    localStorage.setItem('lms.cache', JSON.stringify({ books: 'garbage' }))

    expect(restoredState().books).toBeUndefined()
  })

  it('writes the store to the cache while signed in and clears it on sign-out', () => {
    const store = createStore(signIn('ADMIN'))
    persistOnChange(store)

    store.dispatch({ type: 'books/fetch/fulfilled', payload: { content: [{ id: 1 }], page: 0, size: 10, totalElements: 1, totalPages: 1 } })
    expect(loadCache().books.items).toEqual([{ id: 1 }])

    store.dispatch({ type: 'auth/logout/fulfilled' })
    expect(loadCache()).toBeNull()
  })

  it('clearCache removes the entry', () => {
    saveCache({ books: cachedBooks, members: cachedBooks })
    clearCache()
    expect(loadCache()).toBeNull()
  })
})
