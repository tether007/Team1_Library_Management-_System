import { createSlice } from '@reduxjs/toolkit'
import { logout } from '../auth/authActions'
import { createMember, fetchMembers } from './membersActions'

const initialState = { items: [] }

const membersSlice = createSlice({
  name: 'members',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMembers.fulfilled, (state, action) => {
        state.items = action.payload
      })
      .addCase(createMember.fulfilled, (state, action) => {
        state.items.push(action.payload)
      })
      .addCase(logout.fulfilled, () => initialState)
  },
})

export default membersSlice.reducer
