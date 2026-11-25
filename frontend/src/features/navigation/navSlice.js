import { createSlice } from '@reduxjs/toolkit'
import { login, logout } from '../auth/authActions'

const navSlice = createSlice({
  name: 'nav',
  initialState: { tab: 'books' },
  reducers: {
    setTab(state, action) {
      state.tab = action.payload
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.fulfilled, (state) => {
        state.tab = 'books'
      })
      .addCase(logout.fulfilled, (state) => {
        state.tab = 'books'
      })
  },
})

export const { setTab } = navSlice.actions
export default navSlice.reducer
