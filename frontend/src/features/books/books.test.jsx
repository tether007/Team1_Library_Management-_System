import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { libraryApi } from '../../api/libraryApi'
import { apiError, book, createStoreAs, pageOf, renderWithStore } from '../../test/helpers'
import { createBook, fetchBooks } from './booksActions'
import BooksPage from './BooksPage'

vi.mock('../../api/libraryApi')

describe('books actions', () => {
  it('stores the page of books and its paging info', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')], { page: 1, totalElements: 11, totalPages: 2 }))
    const store = createStoreAs('MEMBER')

    await store.dispatch(fetchBooks({ query: 'clean', page: 1, size: 10, sort: 'title,asc' }))

    expect(libraryApi.getBooks).toHaveBeenCalledWith({ query: 'clean', page: 1, size: 10, sort: 'title,asc' })
    expect(store.getState().books.items.map((b) => b.title)).toEqual(['Clean Code'])
    expect(store.getState().books.pageInfo).toEqual({ page: 1, size: 10, totalElements: 11, totalPages: 2 })
  })

  it('reports a duplicate ISBN from the backend', async () => {
    libraryApi.addBook.mockRejectedValue(apiError('A book with ISBN 1 already exists.'))
    const store = createStoreAs('LIBRARIAN')

    await store.dispatch(createBook({ title: 'X', author: 'Y', isbn: '1' }))

    expect(store.getState().notice.message).toEqual({ type: 'error', text: 'A book with ISBN 1 already exists.' })
  })
})

describe('BooksPage', () => {
  it('lets staff add a book and reloads the list', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')]))
    libraryApi.addBook.mockResolvedValue(book(2, 'Refactoring'))
    const user = userEvent.setup()
    renderWithStore(<BooksPage />, 'LIBRARIAN')

    expect(await screen.findByText('Clean Code')).toBeInTheDocument()
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code'), book(2, 'Refactoring')]))

    await user.type(screen.getByLabelText('Title'), 'Refactoring')
    await user.type(screen.getByLabelText('Author'), 'Martin Fowler')
    await user.type(screen.getByLabelText('ISBN'), '9780134757599')
    await user.click(screen.getByRole('button', { name: 'Add book' }))

    expect(libraryApi.addBook).toHaveBeenCalledWith({ title: 'Refactoring', author: 'Martin Fowler', isbn: '9780134757599' })
    expect(await screen.findByText('Refactoring')).toBeInTheDocument()
  })

  it('hides the add form from members', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')]))
    renderWithStore(<BooksPage />, 'MEMBER')

    expect(await screen.findByText('Clean Code')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Add book' })).not.toBeInTheDocument()
  })

  it('asks for the next page and for a new sort order', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')], { totalElements: 12, totalPages: 2 }))
    const user = userEvent.setup()
    renderWithStore(<BooksPage />, 'MEMBER')

    expect(await screen.findByText('Page 1 of 2 (12 total)')).toBeInTheDocument()
    expect(libraryApi.getBooks).toHaveBeenLastCalledWith({ query: '', page: 0, size: 10, sort: 'title,asc' })

    await user.click(screen.getByRole('button', { name: 'Next' }))
    expect(libraryApi.getBooks).toHaveBeenLastCalledWith({ query: '', page: 1, size: 10, sort: 'title,asc' })

    await user.click(screen.getByRole('button', { name: /^Title/ }))
    expect(libraryApi.getBooks).toHaveBeenLastCalledWith({ query: '', page: 0, size: 10, sort: 'title,desc' })

    await user.click(screen.getByRole('button', { name: /^Author/ }))
    expect(libraryApi.getBooks).toHaveBeenLastCalledWith({ query: '', page: 0, size: 10, sort: 'author,asc' })
  })

  it('searches from the first page', async () => {
    libraryApi.getBooks.mockResolvedValue(pageOf([book(1, 'Clean Code')]))
    const user = userEvent.setup()
    renderWithStore(<BooksPage />, 'MEMBER')
    await screen.findByText('Clean Code')

    await user.type(screen.getByLabelText('Search books'), 'java')

    expect(libraryApi.getBooks).toHaveBeenLastCalledWith({ query: 'java', page: 0, size: 10, sort: 'title,asc' })
  })
})
