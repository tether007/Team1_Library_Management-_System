import { createAsyncThunk } from '@reduxjs/toolkit'
import { clearSession, encodeBasicToken, saveSession } from '../../api/authSession'
import { libraryApi } from '../../api/libraryApi'
import { createApiThunk } from '../../app/createApiThunk'

// Verifies the credentials with the backend (HTTP Basic), then keeps the session.
export const login = createApiThunk('auth/login', async ({ username, password }) => {
  const token = encodeBasicToken(username, password)
  const user = await libraryApi.login(token)
  saveSession({ token, user })
  return user
})

export const logout = createAsyncThunk('auth/logout', async () => {
  clearSession()
})
