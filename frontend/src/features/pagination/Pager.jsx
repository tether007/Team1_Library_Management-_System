export default function Pager({ pageInfo, onPage }) {
  const { page, totalPages, totalElements } = pageInfo

  return (
    <div className="pager">
      <button type="button" disabled={page <= 0} onClick={() => onPage(page - 1)}>Previous</button>
      <span>Page {page + 1} of {Math.max(totalPages, 1)} ({totalElements} total)</span>
      <button type="button" disabled={page + 1 >= totalPages} onClick={() => onPage(page + 1)}>Next</button>
    </div>
  )
}
