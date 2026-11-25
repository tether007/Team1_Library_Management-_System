export const PAGE_SIZE = 10

export const emptyPageState = {
  items: [],
  pageInfo: { page: 0, size: PAGE_SIZE, totalElements: 0, totalPages: 0 },
}

// Converts the backend page response into the shape kept in the store.
export const toPageState = ({ content, page, size, totalElements, totalPages }) => ({
  items: content,
  pageInfo: { page, size, totalElements, totalPages },
})

// Sorting helpers: sort state is { field, dir } and the API wants "field,dir".
export const sortParam = (sort) => `${sort.field},${sort.dir}`

export const toggleSort = (sort, field) =>
  sort.field === field
    ? { field, dir: sort.dir === 'asc' ? 'desc' : 'asc' }
    : { field, dir: 'asc' }
