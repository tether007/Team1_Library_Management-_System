import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { can } from '../auth/permissions'
import { createBook, fetchBooks } from './booksActions'

const EMPTY_FORM = { title: '', author: '', isbn: '' }

export default function BooksPage() {
  const dispatch = useDispatch()
  const books = useSelector((state) => state.books.items)
  const role = useSelector((state) => state.auth.user.role)
  const [query, setQuery] = useState('')
  const [form, setForm] = useState(EMPTY_FORM)

  useEffect(() => {
    dispatch(fetchBooks(query))
  }, [dispatch, query])

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await dispatch(createBook(form))
    if (createBook.fulfilled.match(result)) {
      setForm(EMPTY_FORM)
      dispatch(fetchBooks(query))
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
        onChange={(e) => setQuery(e.target.value)}
      />

      <table>
        <thead>
          <tr><th>Title</th><th>Author</th><th>ISBN</th><th>Status</th></tr>
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
    </section>
  )
}
