import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { libraryApi } from '../../api/libraryApi'
import { apiError, createStoreAs, member, pageOf, renderWithStore } from '../../test/helpers'
import { fetchMembers } from './membersActions'
import MembersPage from './MembersPage'

vi.mock('../../api/libraryApi')

describe('members actions', () => {
  it('stores the page of members', async () => {
    libraryApi.getMembers.mockResolvedValue(pageOf([member(1, 'Asha Rao'), member(2, 'Dr. Mehta', 'FACULTY')]))
    const store = createStoreAs('LIBRARIAN')

    await store.dispatch(fetchMembers({ page: 0, size: 10, sort: 'name,asc' }))

    expect(store.getState().members.items.map((m) => m.name)).toEqual(['Asha Rao', 'Dr. Mehta'])
  })

  it('shows the 403 message when the role is not allowed', async () => {
    libraryApi.getMembers.mockRejectedValue(apiError('You do not have permission to do that.'))
    const store = createStoreAs('MEMBER')

    await store.dispatch(fetchMembers({}))

    expect(store.getState().notice.message.text).toBe('You do not have permission to do that.')
  })
})

describe('MembersPage', () => {
  it('lets an admin add a member and reloads the list', async () => {
    libraryApi.getMembers.mockResolvedValue(pageOf([member(1, 'Asha Rao')]))
    libraryApi.addMember.mockResolvedValue(member(3, 'Ravi Kumar'))
    const user = userEvent.setup()
    renderWithStore(<MembersPage />, 'ADMIN')
    await screen.findByText('Asha Rao')

    libraryApi.getMembers.mockResolvedValue(pageOf([member(1, 'Asha Rao'), member(3, 'Ravi Kumar')]))
    await user.type(screen.getByLabelText('Name'), 'Ravi Kumar')
    await user.click(screen.getByRole('button', { name: 'Add member' }))

    expect(libraryApi.addMember).toHaveBeenCalledWith({ name: 'Ravi Kumar', role: 'STUDENT' })
    expect(await screen.findByText('Ravi Kumar')).toBeInTheDocument()
  })

  it('hides the add form from a librarian', async () => {
    libraryApi.getMembers.mockResolvedValue(pageOf([member(1, 'Asha Rao')]))
    renderWithStore(<MembersPage />, 'LIBRARIAN')

    expect(await screen.findByText('Asha Rao')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Add member' })).not.toBeInTheDocument()
  })

  it('sorts by the entity property the backend understands', async () => {
    libraryApi.getMembers.mockResolvedValue(pageOf([member(1, 'Asha Rao')]))
    const user = userEvent.setup()
    renderWithStore(<MembersPage />, 'LIBRARIAN')
    await screen.findByText('Asha Rao')

    await user.click(screen.getByRole('button', { name: /^Type/ }))

    expect(libraryApi.getMembers).toHaveBeenLastCalledWith({ page: 0, size: 10, sort: 'type,asc' })
  })
})
