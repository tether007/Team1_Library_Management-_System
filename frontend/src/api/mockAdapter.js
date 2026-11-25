// In-memory stand-in for the Spring Boot backend, plugged into axios as a custom adapter.
// It mimics HTTP Basic authentication, role checks (401 / 403) and the { message } error body.
// Set VITE_USE_MOCK=false to talk to the real backend instead.
import { AxiosError } from 'axios'

const BORROW_LIMITS = { STUDENT: 3, FACULTY: 5 }
const DELAY_MS = import.meta.env.MODE === 'test' ? 0 : 150

// Demo accounts (the real backend verifies these against its user table).
export const MOCK_USERS = [
  { username: 'admin', password: 'admin123', role: 'ADMIN' },
  { username: 'librarian', password: 'librarian123', role: 'LIBRARIAN' },
  { username: 'member', password: 'member123', role: 'MEMBER' },
]

const seedBooks = () => [
  { id: 1, title: 'Clean Code', author: 'Robert C. Martin', isbn: '9780132350884', available: true, borrowedBy: null },
  { id: 2, title: 'Effective Java', author: 'Joshua Bloch', isbn: '9780134685991', available: true, borrowedBy: null },
  { id: 3, title: 'Head First Java', author: 'Kathy Sierra', isbn: '9781491910771', available: true, borrowedBy: null },
]

const seedMembers = () => [
  { id: 1, name: 'Asha Rao', role: 'STUDENT' },
  { id: 2, name: 'Dr. Mehta', role: 'FACULTY' },
]

let books = seedBooks()
let members = seedMembers()
let nextBookId = 4
let nextMemberId = 3

export function resetMockData() {
  books = seedBooks()
  members = seedMembers()
  nextBookId = 4
  nextMemberId = 3
}

class HttpError extends Error {
  constructor(status, message) {
    super(message)
    this.status = status
  }
}

const borrowedCount = (memberId) => books.filter((b) => b.borrowedBy === memberId).length

const STAFF = ['ADMIN', 'LIBRARIAN']
const ANYONE = ['ADMIN', 'LIBRARIAN', 'MEMBER']

// roles = who may call the route; handle = the controller logic.
const routes = {
  'GET /auth/me': {
    roles: ANYONE,
    handle: ({ user }) => ({ username: user.username, role: user.role }),
  },

  'GET /books': {
    roles: ANYONE,
    handle: ({ params }) => {
      const q = (params?.query ?? '').trim().toLowerCase()
      if (!q) return books
      return books.filter((b) => [b.title, b.author, b.isbn].some((f) => f.toLowerCase().includes(q)))
    },
  },

  'POST /books': {
    roles: STAFF,
    handle: ({ body }) => {
      if (books.some((b) => b.isbn === body.isbn)) {
        throw new HttpError(409, `A book with ISBN ${body.isbn} already exists.`)
      }
      const book = { id: nextBookId++, ...body, available: true, borrowedBy: null }
      books.push(book)
      return book
    },
  },

  'GET /members': {
    roles: STAFF,
    handle: () => members.map((m) => ({ ...m, borrowedCount: borrowedCount(m.id) })),
  },

  'POST /members': {
    roles: ['ADMIN'],
    handle: ({ body }) => {
      const member = { id: nextMemberId++, ...body }
      members.push(member)
      return { ...member, borrowedCount: 0 }
    },
  },

  'POST /borrow/issue': {
    roles: STAFF,
    handle: ({ body }) => {
      const book = books.find((b) => b.id === body.bookId)
      const member = members.find((m) => m.id === body.memberId)
      if (!book) throw new HttpError(404, 'Book not found.')
      if (!member) throw new HttpError(404, 'Invalid member.')
      if (!book.available) throw new HttpError(409, `"${book.title}" is not available.`)
      const limit = BORROW_LIMITS[member.role]
      if (borrowedCount(member.id) >= limit) {
        throw new HttpError(409, `${member.name} has reached the borrow limit of ${limit}.`)
      }
      book.available = false
      book.borrowedBy = member.id
      return book
    },
  },

  'POST /borrow/return': {
    roles: STAFF,
    handle: ({ body }) => {
      const book = books.find((b) => b.id === body.bookId)
      if (!book) throw new HttpError(404, 'Book not found.')
      if (book.available) throw new HttpError(409, `"${book.title}" was not issued.`)
      book.available = true
      book.borrowedBy = null
      return book
    },
  },
}

function authenticate(config) {
  const header = config.headers.get('Authorization') ?? ''
  const [username, password] = header.startsWith('Basic ') ? atob(header.slice(6)).split(':') : []
  const user = MOCK_USERS.find((u) => u.username === username && u.password === password)
  if (!user) {
    const message = config.url === '/auth/me' ? 'Invalid username or password.' : 'Authentication required.'
    throw new HttpError(401, message)
  }
  return user
}

export default async function mockAdapter(config) {
  await new Promise((resolve) => setTimeout(resolve, DELAY_MS))

  const respond = (status, data) => ({
    data: structuredClone(data),
    status,
    statusText: String(status),
    headers: {},
    config,
  })
  const fail = (status, message) => {
    const response = respond(status, { message })
    return new AxiosError(message, AxiosError.ERR_BAD_REQUEST, config, null, response)
  }

  const route = routes[`${config.method.toUpperCase()} ${config.url}`]
  if (!route) throw fail(404, `No mock route for ${config.method} ${config.url}`)

  try {
    const user = authenticate(config)
    if (!route.roles.includes(user.role)) throw new HttpError(403, 'You do not have permission to do that.')
    const body = config.data ? JSON.parse(config.data) : {}
    return respond(200, route.handle({ body, params: config.params, user }))
  } catch (err) {
    if (!(err instanceof HttpError)) throw err
    throw fail(err.status, err.message)
  }
}
