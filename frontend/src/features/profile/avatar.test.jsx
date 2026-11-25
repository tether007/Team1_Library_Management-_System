import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import Avatar from './Avatar'

describe('Avatar', () => {
  it('is labelled with the username', () => {
    render(<Avatar username="librarian" />)
    expect(screen.getByRole('img', { name: 'Profile photo of librarian' })).toBeInTheDocument()
  })

  it('draws the pixel art and honours the size', () => {
    const { container } = render(<Avatar username="admin" size={96} />)
    const svg = container.querySelector('svg')

    expect(svg).toHaveAttribute('width', '96')
    expect(container.querySelectorAll('rect').length).toBeGreaterThan(20)
  })
})
