import { render, screen } from '@testing-library/react'
import { vi } from 'vitest'
import App from './App'

vi.mock('./api', () => ({
  getDashboardData: vi.fn().mockResolvedValue({
    revenue: { value: 372850 },
    quantity: { value: 27 },
    averageOrderValue: { value: 37285 },
    categories: [
      { name: 'Electronics', revenue: 330000 },
      { name: 'Furniture', revenue: 29000 },
      { name: 'Clothing', revenue: 10800 },
      { name: 'Groceries', revenue: 3050 },
    ],
    regions: [
      { name: 'South', revenue: 292200 },
      { name: 'West', revenue: 58250 },
      { name: 'East', revenue: 17000 },
      { name: 'North', revenue: 5400 },
    ],
    orders: [{ order_id: 1010, customer_id: 'C010', category: 'Electronics', total_amount: 130000 }],
    sales: {
      total: 10,
      rows: [{
        order_id: 1010, order_date: '2026-01-10', customer_id: 'C010',
        product_id: 'P010', category: 'Electronics', quantity: 10,
        unit_price: 13000, region: 'South', payment_method: 'UPI', total_amount: 130000,
      }],
    },
  }),
}))

test('shows dashboard metrics after loading', async () => {
  render(<App />)

  const electronics = await screen.findAllByText('Electronics')
  const inr = '\u20B9'

  expect(electronics).toHaveLength(3)
  expect(screen.getByText(`${inr}3,72,850`)).toBeInTheDocument()
  expect(screen.getByText('27')).toBeInTheDocument()
  expect(screen.getByText(`${inr}37,285`)).toBeInTheDocument()
  expect(screen.getAllByText('South')).toHaveLength(2)
  expect(screen.getAllByText(/1010/)).toHaveLength(2)
})
