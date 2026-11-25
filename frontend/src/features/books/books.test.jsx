import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { createStoreAs, renderWithStore } from '../../test/helpers'
import { createBook, fetchBooks } from './booksActions'
import BooksPage from './BooksPage'

describe('books actions', () => {
  it('loads and filters books', async () => {
    const store = createStoreAs('MEMBER')
    await store.dispatch(fetchBooks('java'))
    expect(store.getState().books.items.map((b) => b.title)).toEqual(['Effective Java', 'Head First Java'])
  })

  it('rejects a duplicate ISBN with an error notice', async () => {
    const store = createStoreAs('LIBRARIAN')
    await store.dispatch(createBook({ title: 'X', author: 'Y', isbn: '9780132350884' }))
    expect(store.getState().notice.message).toEqual({
      type: 'error',
      text: 'A book with ISBN 9780132350884 already exists.',
    })
  })

  it('forbids a member from adding books', async () => {
    const store = createStoreAs('MEMBER')
    await store.dispatch(createBook({ title: 'X', author: 'Y', isbn: '1' }))
    expect(store.getState().notice.message.text).toBe('You do not have permission to do that.')
  })
})

describe('BooksPage', () => {
  it('lets staff add a book', async () => {
    const user = userEvent.setup()
    renderWithStore(<BooksPage />, 'LIBRARIAN')

    expect(await screen.findByText('Clean Code')).toBeInTheDocument()
    await user.type(screen.getByLabelText('Title'), 'Refactoring')
    await user.type(screen.getByLabelText('Author'), 'Martin Fowler')
    await user.type(screen.getByLabelText('ISBN'), '9780134757599')
    await user.click(screen.getByRole('button', { name: 'Add book' }))

    expect(await screen.findByText('Refactoring')).toBeInTheDocument()
  })

  it('hides the add form from members', async () => {
    renderWithStore(<BooksPage />, 'MEMBER')

    expect(await screen.findByText('Clean Code')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Add book' })).not.toBeInTheDocument()
  })
})
