import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { createStoreAs, renderWithStore } from '../../test/helpers'
import { createBook, fetchBooks } from '../books/booksActions'
import { issueBook, returnBook } from './borrowActions'
import BorrowPage from './BorrowPage'

describe('borrow actions', () => {
  it('issues then returns a book', async () => {
    const store = createStoreAs('LIBRARIAN')
    await store.dispatch(fetchBooks(''))

    await store.dispatch(issueBook({ bookId: 1, memberId: 1 }))
    expect(store.getState().books.items.find((b) => b.id === 1).available).toBe(false)

    await store.dispatch(returnBook(1))
    expect(store.getState().books.items.find((b) => b.id === 1).available).toBe(true)
  })

  it('refuses to issue a book that is already issued', async () => {
    const store = createStoreAs('LIBRARIAN')
    await store.dispatch(issueBook({ bookId: 1, memberId: 1 }))
    await store.dispatch(issueBook({ bookId: 1, memberId: 2 }))
    expect(store.getState().notice.message.text).toBe('"Clean Code" is not available.')
  })

  it('refuses to return a book that is not issued', async () => {
    const store = createStoreAs('LIBRARIAN')
    await store.dispatch(returnBook(1))
    expect(store.getState().notice.message.text).toBe('"Clean Code" was not issued.')
  })

  it('enforces the student borrow limit of 3', async () => {
    const store = createStoreAs('ADMIN')
    await store.dispatch(createBook({ title: 'Fourth', author: 'A', isbn: '1' }))
    for (const bookId of [1, 2, 3]) await store.dispatch(issueBook({ bookId, memberId: 1 }))
    await store.dispatch(issueBook({ bookId: 4, memberId: 1 }))
    expect(store.getState().notice.message.text).toBe('Asha Rao has reached the borrow limit of 3.')
  })

  it('forbids the member role from issuing', async () => {
    const store = createStoreAs('MEMBER')
    await store.dispatch(issueBook({ bookId: 1, memberId: 1 }))
    expect(store.getState().notice.message.text).toBe('You do not have permission to do that.')
  })
})

describe('BorrowPage', () => {
  it('issues a book to a member', async () => {
    const user = userEvent.setup()
    renderWithStore(<BorrowPage />, 'LIBRARIAN')

    await waitFor(() => expect(screen.getByRole('option', { name: 'Clean Code' })).toBeInTheDocument())
    await waitFor(() => expect(screen.getByRole('option', { name: /Asha Rao/ })).toBeInTheDocument())

    await user.selectOptions(screen.getByLabelText('Book'), 'Clean Code')
    await user.selectOptions(screen.getByLabelText('Member'), '1')
    await user.click(screen.getByRole('button', { name: 'Issue book' }))

    expect(await screen.findByRole('button', { name: 'Return' })).toBeInTheDocument()
  })
})
