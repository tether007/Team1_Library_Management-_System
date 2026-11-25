import { createSlice, isAnyOf } from '@reduxjs/toolkit'
import { logout } from '../auth/authActions'
import { issueBook, returnBook } from '../borrow/borrowActions'
import { fetchBooks } from './booksActions'

const initialState = { items: [] }

const booksSlice = createSlice({
  name: 'books',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchBooks.fulfilled, (state, action) => {
        state.items = action.payload
      })
      .addCase(logout.fulfilled, () => initialState)
      .addMatcher(isAnyOf(issueBook.fulfilled, returnBook.fulfilled), (state, action) => {
        const index = state.items.findIndex((b) => b.id === action.payload.id)
        if (index !== -1) state.items[index] = action.payload
      })
  },
})

export default booksSlice.reducer
