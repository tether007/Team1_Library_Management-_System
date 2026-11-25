import { libraryApi } from '../../api/libraryApi'
import { createApiThunk } from '../../app/createApiThunk'

export const fetchBooks = createApiThunk('books/fetch', libraryApi.getBooks)
export const createBook = createApiThunk('books/create', libraryApi.addBook)
