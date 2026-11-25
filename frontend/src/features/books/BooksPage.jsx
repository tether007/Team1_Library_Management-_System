import { useCallback, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { can } from '../auth/permissions'
import Pager from '../pagination/Pager'
import { PAGE_SIZE, sortParam, toggleSort } from '../pagination/pageState'
import SortHeader from '../pagination/SortHeader'
import { createBook, fetchBooks } from './booksActions'

const EMPTY_FORM = { title: '', author: '', isbn: '' }

export default function BooksPage() {
  const dispatch = useDispatch()
  const { items: books, pageInfo } = useSelector((state) => state.books)
  const role = useSelector((state) => state.auth.user.role)
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(0)
  const [sort, setSort] = useState({ field: 'title', dir: 'asc' })
  const [form, setForm] = useState(EMPTY_FORM)

  const load = useCallback(
    () => dispatch(fetchBooks({ query, page, size: PAGE_SIZE, sort: sortParam(sort) })),
    [dispatch, query, page, sort],
  )

  useEffect(() => {
    load()
  }, [load])

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleQuery = (value) => {
    setQuery(value)
    setPage(0)
  }

  const handleSort = (field) => {
    setSort((current) => toggleSort(current, field))
    setPage(0)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await dispatch(createBook(form))
    if (createBook.fulfilled.match(result)) {
      setForm(EMPTY_FORM)
      load()
    }
  }

  return (
    <section>
      <h2>Books</h2>

      {can(role, 'books:add') && (
        <form className="row" onSubmit={handleSubmit}>
          <input name="title" placeholder="Title" aria-label="Title" value={form.title} onChange={handleChange} required />
          <input name="author" placeholder="Author" aria-label="Author" value={form.author} onChange={handleChange} required />
          <input name="isbn" placeholder="ISBN" aria-label="ISBN" value={form.isbn} onChange={handleChange} required />
          <button type="submit">Add book</button>
        </form>
      )}

      <input
        className="search"
        placeholder="Search by title, author or ISBN"
        aria-label="Search books"
        value={query}
        onChange={(e) => handleQuery(e.target.value)}
      />

      <table>
        <thead>
          <tr>
            <SortHeader label="Title" field="title" sort={sort} onSort={handleSort} />
            <SortHeader label="Author" field="author" sort={sort} onSort={handleSort} />
            <SortHeader label="ISBN" field="isbn" sort={sort} onSort={handleSort} />
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book) => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{book.isbn}</td>
              <td><span className={book.available ? 'badge ok' : 'badge busy'}>{book.available ? 'Available' : 'Issued'}</span></td>
            </tr>
          ))}
          {books.length === 0 && <tr><td colSpan="4">No books found.</td></tr>}
        </tbody>
      </table>

      <Pager pageInfo={pageInfo} onPage={setPage} />
    </section>
  )
}
