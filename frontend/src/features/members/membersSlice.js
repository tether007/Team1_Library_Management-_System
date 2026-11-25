import { createSlice } from '@reduxjs/toolkit'
import { logout } from '../auth/authActions'
import { emptyPageState, toPageState } from '../pagination/pageState'
import { fetchMembers } from './membersActions'

const membersSlice = createSlice({
  name: 'members',
  initialState: emptyPageState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMembers.fulfilled, (state, action) => toPageState(action.payload))
      .addCase(logout.fulfilled, () => emptyPageState)
  },
})

export default membersSlice.reducer
