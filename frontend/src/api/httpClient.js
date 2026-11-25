import axios from 'axios'
import { loadSession } from './authSession'
import mockAdapter from './mockAdapter'

// Mock backend is on by default. Set VITE_USE_MOCK=false to call the real Spring Boot API.
const useMock = import.meta.env.VITE_USE_MOCK !== 'false'

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api',
  headers: { 'Content-Type': 'application/json' },
  ...(useMock && { adapter: mockAdapter }),
})

// Request middleware: attach HTTP Basic credentials of the signed-in user.
http.interceptors.request.use((config) => {
  const session = loadSession()
  if (session?.token && !config.headers.has('Authorization')) {
    config.headers.set('Authorization', `Basic ${session.token}`)
  }
  return config
})

// Response middleware: a 401 on any call other than the login check means the session is no longer valid.
let onUnauthorized = () => {}
export const setUnauthorizedHandler = (handler) => {
  onUnauthorized = handler
}

http.interceptors.response.use(undefined, (error) => {
  if (error.response?.status === 401 && error.config?.url !== '/auth/me') onUnauthorized()
  return Promise.reject(error)
})

export const errorMessage = (err) => err.response?.data?.message ?? err.message
