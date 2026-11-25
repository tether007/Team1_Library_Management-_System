import { useCallback, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { can } from '../auth/permissions'
import Pager from '../pagination/Pager'
import { PAGE_SIZE, sortParam, toggleSort } from '../pagination/pageState'
import SortHeader from '../pagination/SortHeader'
import { createMember, fetchMembers } from './membersActions'

export default function MembersPage() {
  const dispatch = useDispatch()
  const { items: members, pageInfo } = useSelector((state) => state.members)
  const role = useSelector((state) => state.auth.user.role)
  const [name, setName] = useState('')
  const [memberRole, setMemberRole] = useState('STUDENT')
  const [page, setPage] = useState(0)
  const [sort, setSort] = useState({ field: 'name', dir: 'asc' })

  const load = useCallback(
    () => dispatch(fetchMembers({ page, size: PAGE_SIZE, sort: sortParam(sort) })),
    [dispatch, page, sort],
  )

  useEffect(() => {
    load()
  }, [load])

  const handleSort = (field) => {
    setSort((current) => toggleSort(current, field))
    setPage(0)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await dispatch(createMember({ name, role: memberRole }))
    if (createMember.fulfilled.match(result)) {
      setName('')
      load()
    }
  }

  return (
    <section>
      <h2>Members</h2>

      {can(role, 'members:add') && (
        <form className="row" onSubmit={handleSubmit}>
          <input placeholder="Name" aria-label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
          <select aria-label="Member type" value={memberRole} onChange={(e) => setMemberRole(e.target.value)}>
            <option value="STUDENT">Student</option>
            <option value="FACULTY">Faculty</option>
          </select>
          <button type="submit">Add member</button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <SortHeader label="ID" field="id" sort={sort} onSort={handleSort} />
            <SortHeader label="Name" field="name" sort={sort} onSort={handleSort} />
            <SortHeader label="Type" field="type" sort={sort} onSort={handleSort} />
            <th>Books borrowed</th>
          </tr>
        </thead>
        <tbody>
          {members.map((m) => (
            <tr key={m.id}>
              <td>{m.id}</td>
              <td>{m.name}</td>
              <td>{m.role}</td>
              <td>{m.borrowedCount}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <Pager pageInfo={pageInfo} onPage={setPage} />
    </section>
  )
}
