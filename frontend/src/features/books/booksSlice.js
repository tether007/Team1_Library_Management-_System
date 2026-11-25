import { createSlice, isAnyOf } from '@reduxjs/toolkit'
import { logout } from '../auth/authActions'
import { issueBook, returnBook } from '../borrow/borrowActions'
import { emptyPageState, toPageState } from '../pagination/pageState'
import { fetchBooks } from './booksActions'

const booksSlice = createSlice({
  name: 'books',
  initialState: emptyPageState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchBooks.fulfilled, (state, action) => toPageState(action.payload))
      .addCase(logout.fulfilled, () => emptyPageState)
      .addMatcher(isAnyOf(issueBook.fulfilled, returnBook.fulfilled), (state, action) => {
        const index = state.items.findIndex((b) => b.id === action.payload.id)
        if (index !== -1) state.items[index] = action.payload
      })
  },
})

export default booksSlice.reducer
