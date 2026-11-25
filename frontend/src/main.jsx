import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import './index.css'
import App from './App.jsx'
import { setUnauthorizedHandler } from './api/httpClient'
import { persistOnChange } from './app/localCache'
import { store } from './app/store'
import { logout } from './features/auth/authActions'

// Any 401 from the API signs the user out and returns them to the login page.
setUnauthorizedHandler(() => store.dispatch(logout()))

// Keep the localStorage cache of books and members up to date.
persistOnChange(store)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>,
)
