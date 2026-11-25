import { useSelector } from 'react-redux'

export default function Notice() {
  const message = useSelector((state) => state.notice.message)
  if (!message) return null
  return (
    <p className={`notice ${message.type}`} role={message.type === 'error' ? 'alert' : 'status'}>
      {message.text}
    </p>
  )
}
