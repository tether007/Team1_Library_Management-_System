import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeEach } from 'vitest'
import { resetMockData } from '../api/mockAdapter'

beforeEach(resetMockData)
afterEach(() => {
  cleanup()
  sessionStorage.clear()
})
