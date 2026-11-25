import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { libraryApi } from '../../api/libraryApi'
import { apiError, book, createStoreAs, member, pageOf, renderWithStore } from '../../test/helpers'
import { fetchBooks } from '../books/booksActions'
import { issueBook, returnBook } from './borrowActions'
import BorrowPage from './BorrowPage'

vi.mock('../../api/libraryApi')

describe('borrow actions', () => {
  it('replaces the book in the list when it is issued and returned', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')]))
    libraryApi.issueBook.mockResolvedValue(book(1, 'Clean Code', { available: false, borrowedBy: 1 }))
    libraryApi.returnBook.mockResolvedValue(book(1, 'Clean Code'))
    const store = createStoreAs('LIBRARIAN')
    await store.dispatch(fetchBooks({}))

    await store.dispatch(issueBook({ bookId: 1, memberId: 1 }))
    expect(libraryApi.issueBook).toHaveBeenCalledWith({ bookId: 1, memberId: 1 })
    expect(store.getState().books.items[0].available).toBe(false)
    expect(store.getState().notice.message).toEqual({ type: 'success', text: 'Book issued.' })

    await store.dispatch(returnBook(1))
    expect(store.getState().books.items[0].available).toBe(true)
  })

  it('shows the rule violation returned by the backend', async () => {
    libraryApi.issueBook.mockRejectedValue(apiError('Asha Rao has reached the borrow limit of 3.'))
    const store = createStoreAs('LIBRARIAN')

    await store.dispatch(issueBook({ bookId: 4, memberId: 1 }))

    expect(store.getState().notice.message).toEqual({
      type: 'error',
      text: 'Asha Rao has reached the borrow limit of 3.',
    })
  })
})

describe('BorrowPage', () => {
  it('issues a book to a member', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')]))
    libraryApi.getMembers.mockResolvedValue(pageOf([member(1, 'Asha Rao')]))
    libraryApi.issueBook.mockResolvedValue(book(1, 'Clean Code', { available: false, borrowedBy: 1 }))
    const user = userEvent.setup()
    renderWithStore(<BorrowPage />, 'LIBRARIAN')

    await waitFor(() => expect(screen.getByRole('option', { name: 'Clean Code' })).toBeInTheDocument())
    await waitFor(() => expect(screen.getByRole('option', { name: /Asha Rao/ })).toBeInTheDocument())

    await user.selectOptions(screen.getByLabelText('Book'), 'Clean Code')
    await user.selectOptions(screen.getByLabelText('Member'), '1')
    await user.click(screen.getByRole('button', { name: 'Issue book' }))

    expect(await screen.findByRole('button', { name: 'Return' })).toBeInTheDocument()
    expect(libraryApi.getBooks).toHaveBeenCalledWith({ page: 0, size: 100, sort: 'title,asc' })
  })
})
