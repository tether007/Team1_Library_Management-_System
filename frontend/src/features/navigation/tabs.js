import { can } from '../auth/permissions'

const TABS = [
  { id: 'books', label: 'Books', ability: 'books:view' },
  { id: 'members', label: 'Members', ability: 'members:view' },
  { id: 'borrow', label: 'Issue / Return', ability: 'borrow:manage' },
]

export const tabsFor = (role) => TABS.filter((tab) => can(role, tab.ability))
