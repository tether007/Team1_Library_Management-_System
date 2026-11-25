import { createSlice } from '@reduxjs/toolkit'
import { login, logout } from './authActions'

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(login.fulfilled, (state, action) => {
        state.user = action.payload
      })
      .addCase(logout.fulfilled, (state) => {
        state.user = null
      })
  },
})

export default authSlice.reducer
