// Role-based access control. The backend enforces the same rules; this only decides what the UI shows.
const ABILITIES = {
  ADMIN: ['books:view', 'books:add', 'members:view', 'members:add', 'borrow:manage'],
  LIBRARIAN: ['books:view', 'books:add', 'members:view', 'borrow:manage'],
  MEMBER: ['books:view'],
}

export const can = (role, ability) => ABILITIES[role]?.includes(ability) ?? false
