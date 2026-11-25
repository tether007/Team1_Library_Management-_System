import { http } from './httpClient'

// One function per Spring Boot endpoint. List calls take { page, size, sort } (sort is "field,asc|desc")
// and resolve to { content, page, size, totalElements, totalPages }.
export const libraryApi = {
  login: (token) =>
    http.get('/auth/me', { headers: { Authorization: `Basic ${token}` } }).then((r) => r.data),
  getBooks: ({ query = '', page = 0, size = 10, sort } = {}) =>
    http.get('/books', { params: { query, page, size, sort } }).then((r) => r.data),
  addBook: (book) => http.post('/books', book).then((r) => r.data),
  getMembers: ({ page = 0, size = 10, sort } = {}) =>
    http.get('/members', { params: { page, size, sort } }).then((r) => r.data),
  addMember: (member) => http.post('/members', member).then((r) => r.data),
  issueBook: ({ bookId, memberId }) => http.post('/borrow/issue', { bookId, memberId }).then((r) => r.data),
  returnBook: (bookId) => http.post('/borrow/return', { bookId }).then((r) => r.data),
}
