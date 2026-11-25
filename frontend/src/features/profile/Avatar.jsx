// Default profile photo: an 8x8 pixel-art face drawn as SVG squares, so it needs no image file and
// stays sharp at any size. A real uploaded photo can replace it later through the same component.
// '#' = black, 'y' = light yellow, '.' = empty.
const PIXELS = [
  '..####..',
  '.######.',
  '.#yyyy#.',
  '.y#yy#y.',
  '.yyyyyy.',
  '..y##y..',
  '..yyyy..',
  '.######.',
]

const COLORS = { '#': 'var(--black)', y: 'var(--light-yellow)' }

export default function Avatar({ username, size = 72 }) {
  return (
    <svg
      className="avatar"
      role="img"
      aria-label={`Profile photo of ${username}`}
      viewBox="0 0 8 8"
      width={size}
      height={size}
      shapeRendering="crispEdges"
    >
      {PIXELS.flatMap((row, y) =>
        [...row].map((cell, x) =>
          COLORS[cell] ? <rect key={`${x}-${y}`} x={x} y={y} width="1" height="1" style={{ fill: COLORS[cell] }} /> : null,
        ),
      )}
    </svg>
  )
}
