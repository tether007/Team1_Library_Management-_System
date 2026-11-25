import { createAsyncThunk } from '@reduxjs/toolkit'
import { errorMessage } from '../api/httpClient'

// Wraps an API call so failures reach the store as a plain message string.
export const createApiThunk = (type, call) =>
  createAsyncThunk(type, async (arg, { rejectWithValue }) => {
    try {
      return await call(arg)
    } catch (err) {
      return rejectWithValue(errorMessage(err))
    }
  })
