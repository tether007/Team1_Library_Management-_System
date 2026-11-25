import { configureStore } from '@reduxjs/toolkit'
import { loadSession } from '../api/authSession'
import authReducer from '../features/auth/authSlice'
import booksReducer from '../features/books/booksSlice'
import membersReducer from '../features/members/membersSlice'
import navReducer from '../features/navigation/navSlice'
import noticeReducer from '../features/notice/noticeSlice'

export const createStore = (preloadedState) =>
  configureStore({
    reducer: {
      auth: authReducer,
      books: booksReducer,
      members: membersReducer,
      nav: navReducer,
      notice: noticeReducer,
    },
    preloadedState,
  })

// The app store restores a previous session on page refresh.
export const store = createStore({ auth: { user: loadSession()?.user ?? null } })
