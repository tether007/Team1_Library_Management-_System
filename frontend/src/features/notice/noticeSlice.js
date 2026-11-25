import { createSlice, isAnyOf, isRejected } from '@reduxjs/toolkit'
import { login, logout } from '../auth/authActions'
import { createBook } from '../books/booksActions'
import { issueBook, returnBook } from '../borrow/borrowActions'
import { createMember } from '../members/membersActions'
import { setTab } from '../navigation/navSlice'

const SUCCESS_MESSAGES = {
  [createBook.fulfilled.type]: 'Book added.',
  [createMember.fulfilled.type]: 'Member added.',
  [issueBook.fulfilled.type]: 'Book issued.',
  [returnBook.fulfilled.type]: 'Book returned.',
}

// Holds the single banner message ({ type: 'success' | 'error', text }) shown above the page.
const noticeSlice = createSlice({
  name: 'notice',
  initialState: { message: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(setTab, (state) => {
        state.message = null
      })
      .addCase(login.fulfilled, (state) => {
        state.message = null
      })
      .addCase(logout.fulfilled, (state) => {
        state.message = null
      })
      .addMatcher(isRejected, (state, action) => {
        state.message = { type: 'error', text: action.payload ?? action.error.message }
      })
      .addMatcher(
        isAnyOf(createBook.fulfilled, createMember.fulfilled, issueBook.fulfilled, returnBook.fulfilled),
        (state, action) => {
          state.message = { type: 'success', text: SUCCESS_MESSAGES[action.type] }
        },
      )
  },
})

export default noticeSlice.reducer
