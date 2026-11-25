import { libraryApi } from '../../api/libraryApi'
import { createApiThunk } from '../../app/createApiThunk'

export const fetchMembers = createApiThunk('members/fetch', libraryApi.getMembers)
export const createMember = createApiThunk('members/create', libraryApi.addMember)
