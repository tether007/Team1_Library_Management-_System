import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchBooks } from '../books/booksActions'
import { fetchMembers } from '../members/membersActions'
import { issueBook, returnBook } from './borrowActions'

export default function BorrowPage() {
  const dispatch = useDispatch()
  const books = useSelector((state) => state.books.items)
  const members = useSelector((state) => state.members.items)
  const [bookId, setBookId] = useState('')
  const [memberId, setMemberId] = useState('')

  useEffect(() => {
    dispatch(fetchBooks(''))
    dispatch(fetchMembers())
  }, [dispatch])

  const available = books.filter((b) => b.available)
  const issued = books.filter((b) => !b.available)
  const memberName = (id) => members.find((m) => m.id === id)?.name ?? `#${id}`

  const handleIssue = async (e) => {
    e.preventDefault()
    const result = await dispatch(issueBook({ bookId: Number(bookId), memberId: Number(memberId) }))
    if (issueBook.fulfilled.match(result)) {
      setBookId('')
      dispatch(fetchMembers())
    }
  }

  const handleReturn = async (id) => {
    await dispatch(returnBook(id))
    dispatch(fetchMembers())
  }

  return (
    <section>
      <h2>Issue / Return</h2>

      <form className="row" onSubmit={handleIssue}>
        <select aria-label="Book" value={bookId} onChange={(e) => setBookId(e.target.value)} required>
          <option value="">Select available book</option>
          {available.map((b) => <option key={b.id} value={b.id}>{b.title}</option>)}
        </select>
        <select aria-label="Member" value={memberId} onChange={(e) => setMemberId(e.target.value)} required>
          <option value="">Select member</option>
          {members.map((m) => <option key={m.id} value={m.id}>{m.name} ({m.role})</option>)}
        </select>
        <button type="submit">Issue book</button>
      </form>

      <h3>Currently issued</h3>
      <table>
        <thead>
          <tr><th>Title</th><th>Borrowed by</th><th></th></tr>
        </thead>
        <tbody>
          {issued.map((b) => (
            <tr key={b.id}>
              <td>{b.title}</td>
              <td>{memberName(b.borrowedBy)}</td>
              <td><button onClick={() => handleReturn(b.id)}>Return</button></td>
            </tr>
          ))}
          {issued.length === 0 && <tr><td colSpan="3">No books are issued.</td></tr>}
        </tbody>
      </table>
    </section>
  )
}
