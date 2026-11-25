import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import { libraryApi } from './api/libraryApi'
import { book, pageOf, renderWithStore } from './test/helpers'

vi.mock('./api/libraryApi')

describe('App', () => {
  it('shows the login page when signed out', () => {
    renderWithStore(<App />)
    expect(screen.getByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
  })

  it('lands on the book list after signing in as a member, with no staff views', async () => {
    libraryApi.login.mockResolvedValue({ username: 'member', role: 'MEMBER' })
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')]))
    const user = userEvent.setup()
    renderWithStore(<App />)

    await user.type(screen.getByLabelText('Username'), 'member')
    await user.type(screen.getByLabelText('Password'), 'member123')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByText('Clean Code')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Members' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Issue / Return' })).not.toBeInTheDocument()
  })

  it('returns to the login page after signing out', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([]))
    const user = userEvent.setup()
    renderWithStore(<App />, 'ADMIN')

    await user.click(screen.getByRole('button', { name: 'Sign out' }))
    expect(await screen.findByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
  })
})
