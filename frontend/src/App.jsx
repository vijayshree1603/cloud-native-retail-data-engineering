import { useEffect, useState } from 'react'
import { getDashboardData } from './api'

const money = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  maximumFractionDigits: 0,
})

const number = new Intl.NumberFormat('en-IN')

function BarChart({ title, data = [] }) {
  const max = Math.max(...data.map((item) => Number(item.revenue)), 1)

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>{title}</h2>
      </div>

      {data.length === 0 ? (
        <p className="empty">No sales data yet.</p>
      ) : (
        <div className="bar-list">
          {data.map((item) => (
            <div className="bar-row" key={item.name}>
              <div className="bar-label">
                <span>{item.name}</span>
                <strong>{money.format(item.revenue)}</strong>
              </div>

              <div className="bar-track">
                <i
                  style={{
                    width: `${(Number(item.revenue) / max) * 100}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

function OrderTable({ rows = [], compact = false }) {
  if (!rows.length) {
    return (
      <p className="empty">
        No sales have been loaded. Run the ETL pipeline to populate the dashboard.
      </p>
    )
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Order</th>
            <th>Customer</th>
            <th>Category</th>
            {!compact && <th>Date</th>}
            {!compact && <th>Region</th>}
            {!compact && <th>Qty</th>}
            <th>Value</th>
          </tr>
        </thead>

        <tbody>
          {rows.map((row) => (
            <tr key={row.order_id}>
              <td>#{row.order_id}</td>
              <td>{row.customer_id}</td>
              <td>{row.category}</td>

              {!compact && <td>{row.order_date}</td>}
              {!compact && <td>{row.region}</td>}
              {!compact && <td>{row.quantity}</td>}

              <td>{money.format(row.total_amount)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DataState({ error, children }) {
  if (error) {
    return (
      <div className="error-state">
        <strong>Dashboard unavailable</strong>
        <span>{error}</span>
      </div>
    )
  }

  return children
}

export default function App() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getDashboardData()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return (
      <main className="app">
        <DataState error={error} />
      </main>
    )
  }

  if (!data) {
    return (
      <main className="app">
        <div className="loading">Loading retail analytics...</div>
      </main>
    )
  }

  const {
    revenue = { value: 0 },
    quantity = { value: 0 },
    averageOrderValue = { value: 0 },
    categories = [],
    regions = [],
    orders = [],
    sales = { total: 0, rows: [] },
  } = data

  return (
    <main className="app">
      <header className="hero">
        <div>
          <span className="eyebrow">COMMERCE INTELLIGENCE</span>
          <h1>Retail Analytics</h1>
          <p>
            A real-time view of ETL-loaded sales performance.
          </p>
        </div>

        <div className="status">
          <span className="status-dot" />
          Data connected
        </div>
      </header>

      <section className="kpi-grid">
        <article className="kpi-card">
          <span>Total revenue</span>
          <strong>{money.format(revenue.value)}</strong>
        </article>

        <article className="kpi-card">
          <span>Quantity sold</span>
          <strong>{number.format(quantity.value)}</strong>
        </article>

        <article className="kpi-card">
          <span>Average order value</span>
          <strong>{money.format(averageOrderValue.value)}</strong>
        </article>
      </section>

      <section className="chart-grid">
        <BarChart
          title="Revenue by category"
          data={categories}
        />

        <BarChart
          title="Revenue by region"
          data={regions}
        />
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Highest-value orders</h2>
            <p>Top-performing transactions</p>
          </div>
        </div>

        <OrderTable rows={orders} compact />
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Sales data</h2>
            <p>{sales.total} records</p>
          </div>
        </div>

        <OrderTable rows={sales.rows} />
      </section>
    </main>
  )
}