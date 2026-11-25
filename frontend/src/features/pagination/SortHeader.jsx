// A table header that sorts by `field` when clicked. `sort` is the current { field, dir }.
export default function SortHeader({ label, field, sort, onSort }) {
  const active = sort.field === field
  const ariaSort = active ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'

  return (
    <th aria-sort={ariaSort}>
      <button type="button" className="sort" onClick={() => onSort(field)}>
        {label}{active ? (sort.dir === 'asc' ? ' ▲' : ' ▼') : ''}
      </button>
    </th>
  )
}
