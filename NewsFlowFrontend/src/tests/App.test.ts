import { render } from '@testing-library/svelte'
import { describe, it, expect } from 'vitest'
import App from '../App.svelte'

describe('App.svelte', () => {
  it('renders settings button', () => {
    const { getByText } = render(App)
    const button = getByText(/settings/i)
    expect(button).toBeInTheDocument()
  })
})
