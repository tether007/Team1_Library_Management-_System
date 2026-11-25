import { http } from './httpClient'

// One function per planned Spring Boot endpoint.
export const libraryApi = {
  login: (token) =>
    http.get('/auth/me', { headers: { Authorization: `Basic ${token}` } }).then((r) => r.data),
  getBooks: (query = '') => http.get('/books', { params: { query } }).then((r) => r.data),
  addBook: (book) => http.post('/books', book).then((r) => r.data),
  getMembers: () => http.get('/members').then((r) => r.data),
  addMember: (member) => http.post('/members', member).then((r) => r.data),
  issueBook: ({ bookId, memberId }) => http.post('/borrow/issue', { bookId, memberId }).then((r) => r.data),
  returnBook: (bookId) => http.post('/borrow/return', { bookId }).then((r) => r.data),
}
