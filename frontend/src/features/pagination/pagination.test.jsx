import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import Pager from './Pager'
import { sortParam, toggleSort, toPageState } from './pageState'
import SortHeader from './SortHeader'

describe('pageState', () => {
  it('converts a backend page into store state', () => {
    expect(toPageState({ content: [1], page: 2, size: 10, totalElements: 21, totalPages: 3 })).toEqual({
      items: [1],
      pageInfo: { page: 2, size: 10, totalElements: 21, totalPages: 3 },
    })
  })

  it('toggles direction on the same field and starts ascending on a new one', () => {
    expect(toggleSort({ field: 'title', dir: 'asc' }, 'title')).toEqual({ field: 'title', dir: 'desc' })
    expect(toggleSort({ field: 'title', dir: 'desc' }, 'author')).toEqual({ field: 'author', dir: 'asc' })
    expect(sortParam({ field: 'author', dir: 'desc' })).toBe('author,desc')
  })
})

describe('Pager', () => {
  it('disables Previous on the first page and Next on the last', () => {
    const { rerender } = render(<Pager pageInfo={{ page: 0, totalPages: 2, totalElements: 12 }} onPage={() => {}} />)
    expect(screen.getByRole('button', { name: 'Previous' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Next' })).toBeEnabled()

    rerender(<Pager pageInfo={{ page: 1, totalPages: 2, totalElements: 12 }} onPage={() => {}} />)
    expect(screen.getByRole('button', { name: 'Next' })).toBeDisabled()
  })

  it('reports the requested page', async () => {
    const onPage = vi.fn()
    render(<Pager pageInfo={{ page: 1, totalPages: 3, totalElements: 25 }} onPage={onPage} />)

    await userEvent.click(screen.getByRole('button', { name: 'Next' }))
    await userEvent.click(screen.getByRole('button', { name: 'Previous' }))

    expect(onPage).toHaveBeenNthCalledWith(1, 2)
    expect(onPage).toHaveBeenNthCalledWith(2, 0)
  })

  it('shows page 1 of 1 when there are no results', () => {
    render(<Pager pageInfo={{ page: 0, totalPages: 0, totalElements: 0 }} onPage={() => {}} />)
    expect(screen.getByText('Page 1 of 1 (0 total)')).toBeInTheDocument()
  })
})

describe('SortHeader', () => {
  const renderHeader = (sort, onSort = () => {}) =>
    render(
      <table>
        <thead>
          <tr><SortHeader label="Title" field="title" sort={sort} onSort={onSort} /></tr>
        </thead>
      </table>,
    )

  it('marks the active column with its direction', () => {
    renderHeader({ field: 'title', dir: 'desc' })
    expect(screen.getByRole('columnheader')).toHaveAttribute('aria-sort', 'descending')
  })

  it('is not marked when another column is sorted, and reports clicks', async () => {
    const onSort = vi.fn()
    renderHeader({ field: 'author', dir: 'asc' }, onSort)
    expect(screen.getByRole('columnheader')).toHaveAttribute('aria-sort', 'none')

    await userEvent.click(screen.getByRole('button', { name: 'Title' }))
    expect(onSort).toHaveBeenCalledWith('title')
  })
})
