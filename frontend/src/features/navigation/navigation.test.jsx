import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { renderWithStore } from '../../test/helpers'
import Navbar from './Navbar'
import { tabsFor } from './tabs'

describe('tabsFor', () => {
  it('returns the views each role may open', () => {
    expect(tabsFor('ADMIN').map((t) => t.id)).toEqual(['books', 'members', 'borrow'])
    expect(tabsFor('LIBRARIAN').map((t) => t.id)).toEqual(['books', 'members', 'borrow'])
    expect(tabsFor('MEMBER').map((t) => t.id)).toEqual(['books'])
  })
})

describe('Navbar', () => {
  it('shows only permitted tabs and the signed-in user', () => {
    renderWithStore(<Navbar />, 'MEMBER')

    expect(screen.getByText('member [MEMBER]')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Books' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Members' })).not.toBeInTheDocument()
  })

  it.each(['ADMIN', 'LIBRARIAN', 'MEMBER'])('shows the profile photo below Sign out for %s', (role) => {
    renderWithStore(<Navbar />, role)

    const signOut = screen.getByRole('button', { name: 'Sign out' })
    const photo = screen.getByRole('img', { name: `Profile photo of ${role.toLowerCase()}` })

    expect(signOut.compareDocumentPosition(photo) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('switches tab and signs out', async () => {
    const user = userEvent.setup()
    const { store } = renderWithStore(<Navbar />, 'ADMIN')

    await user.click(screen.getByRole('button', { name: 'Members' }))
    expect(store.getState().nav.tab).toBe('members')

    await user.click(screen.getByRole('button', { name: 'Sign out' }))
    await waitFor(() => expect(store.getState().auth.user).toBeNull())
  })
})
