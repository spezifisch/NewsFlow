import { render, fireEvent } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import ConfigDialog from '../components/ConfigDialog.svelte';
import { writable } from 'svelte/store';

describe('ConfigDialog.svelte', () => {
  it('opens and closes the config dialog', async () => {
    // Mock the show store
    const show = writable(true);
    const { getByText, getByPlaceholderText, component } = render(ConfigDialog, {
      props: { show }
    });

    // Check if the dialog is open
    const saveButton = getByText(/save/i);
    expect(saveButton).toBeInTheDocument();

    // Check if the input is rendered
    const patInput = getByPlaceholderText(/enter your pat here/i);
    expect(patInput).toBeInTheDocument();

    // Click the save button
    await fireEvent.click(saveButton);

    // Check if the dialog is closed
    show.subscribe(value => {
      expect(value).toBe(false);
    });
  });
});
