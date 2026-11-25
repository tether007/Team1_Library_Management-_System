import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { createStoreAs, renderWithStore } from '../../test/helpers'
import { fetchMembers } from './membersActions'
import MembersPage from './MembersPage'

describe('members actions', () => {
  it('loads members for staff', async () => {
    const store = createStoreAs('LIBRARIAN')
    await store.dispatch(fetchMembers())
    expect(store.getState().members.items.map((m) => m.name)).toEqual(['Asha Rao', 'Dr. Mehta'])
  })

  it('forbids the member role from listing members', async () => {
    const store = createStoreAs('MEMBER')
    await store.dispatch(fetchMembers())
    expect(store.getState().notice.message.text).toBe('You do not have permission to do that.')
  })
})

describe('MembersPage', () => {
  it('lets an admin add a member', async () => {
    const user = userEvent.setup()
    renderWithStore(<MembersPage />, 'ADMIN')

    await user.type(await screen.findByLabelText('Name'), 'Ravi Kumar')
    await user.click(screen.getByRole('button', { name: 'Add member' }))

    expect(await screen.findByText('Ravi Kumar')).toBeInTheDocument()
  })

  it('hides the add form from a librarian', async () => {
    renderWithStore(<MembersPage />, 'LIBRARIAN')

    expect(await screen.findByText('Asha Rao')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Add member' })).not.toBeInTheDocument()
  })
})
