import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/svelte'
import App from '../App.svelte'

describe('App.svelte', () => {
  it('renders settings button', () => {
    const { getByText } = render(App)
    expect(getByText('Settings')).toBeTruthy()
  })
})
