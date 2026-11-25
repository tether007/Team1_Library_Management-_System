// Keeps the Basic-auth token and signed-in user in sessionStorage so a page refresh keeps the session.
const KEY = 'lms.session'

export const encodeBasicToken = (username, password) => btoa(`${username}:${password}`)

export const loadSession = () => {
  try {
    return JSON.parse(sessionStorage.getItem(KEY))
  } catch {
    return null
  }
}

export const saveSession = (session) => sessionStorage.setItem(KEY, JSON.stringify(session))

export const clearSession = () => sessionStorage.removeItem(KEY)
