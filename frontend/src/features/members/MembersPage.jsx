import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { can } from '../auth/permissions'
import { createMember, fetchMembers } from './membersActions'

export default function MembersPage() {
  const dispatch = useDispatch()
  const members = useSelector((state) => state.members.items)
  const role = useSelector((state) => state.auth.user.role)
  const [name, setName] = useState('')
  const [memberRole, setMemberRole] = useState('STUDENT')

  useEffect(() => {
    dispatch(fetchMembers())
  }, [dispatch])

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await dispatch(createMember({ name, role: memberRole }))
    if (createMember.fulfilled.match(result)) setName('')
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
          <tr><th>ID</th><th>Name</th><th>Type</th><th>Books borrowed</th></tr>
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
    </section>
  )
}
