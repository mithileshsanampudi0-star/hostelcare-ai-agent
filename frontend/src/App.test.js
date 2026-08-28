import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the complaint reporting screen', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /hostelcare ai/i })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: /report an issue/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /check status/i })).toBeInTheDocument();
});
