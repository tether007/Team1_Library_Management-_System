import { libraryApi } from '../../api/libraryApi'
import { createApiThunk } from '../../app/createApiThunk'

export const issueBook = createApiThunk('borrow/issue', libraryApi.issueBook)
export const returnBook = createApiThunk('borrow/return', libraryApi.returnBook)
