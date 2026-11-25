import { configureStore } from '@reduxjs/toolkit'
import authReducer from '../features/auth/authSlice'
import booksReducer from '../features/books/booksSlice'
import membersReducer from '../features/members/membersSlice'
import navReducer from '../features/navigation/navSlice'
import noticeReducer from '../features/notice/noticeSlice'
import { restoredState } from './localCache'

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

// The app store restores the previous session and cached lists on page refresh.
export const store = createStore(restoredState())
