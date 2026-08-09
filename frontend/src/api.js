// The production container leaves this empty so requests are proxied by Nginx.
// Local Vite development still defaults to the directly exposed API port.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function getJson(path) {
  const response = await fetch(`${API_URL}${path}`)
  if (!response.ok) throw new Error(`Request failed (${response.status})`)
  return response.json()
}

export async function getDashboardData() {
  const [revenue, quantity, averageOrderValue, categories, regions, orders, sales] = await Promise.all([
    getJson('/api/analytics/total-revenue'), getJson('/api/analytics/total-quantity'),
    getJson('/api/analytics/average-order-value'), getJson('/api/analytics/revenue-by-category'),
    getJson('/api/analytics/revenue-by-region'), getJson('/api/analytics/highest-value-orders'), getJson('/api/sales?limit=25'),
  ])
  return { revenue, quantity, averageOrderValue, categories, regions, orders, sales }
}
