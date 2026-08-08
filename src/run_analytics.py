"""Analytics queries for the loaded retail sales table."""

import sqlite3

from src.config import DATABASE_PATH
from src.logger import get_logger


def run_query(connection, title, query):
    """Print and return results for one named SQL query."""
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")
    cursor = connection.execute(query)
    print([description[0] for description in cursor.description])
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows


def run_analytics(database_path=DATABASE_PATH):
    """Run the standard analytics queries and return their result rows."""
    connection = sqlite3.connect(str(database_path))
    try:
        table_exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'retail_sales'"
        ).fetchone()
        if not table_exists:
            raise RuntimeError("retail_sales table does not exist. Run the load step first.")

        queries = {
            "total_revenue": ("1. Total Revenue", "SELECT SUM(total_amount) AS total_revenue FROM retail_sales"),
            "revenue_by_category": ("2. Revenue by Category", "SELECT category, SUM(total_amount) AS revenue FROM retail_sales GROUP BY category ORDER BY revenue DESC"),
            "revenue_by_region": ("3. Revenue by Region", "SELECT region, SUM(total_amount) AS revenue FROM retail_sales GROUP BY region ORDER BY revenue DESC"),
            "total_quantity": ("4. Total Quantity Sold", "SELECT SUM(quantity) AS total_quantity FROM retail_sales"),
            "average_order_value": ("5. Average Order Value", "SELECT AVG(total_amount) AS average_order_value FROM retail_sales"),
            "highest_value_orders": ("6. Highest Value Orders", "SELECT order_id, customer_id, category, total_amount FROM retail_sales ORDER BY total_amount DESC LIMIT 5"),
        }
        results = {name: run_query(connection, title, query) for name, (title, query) in queries.items()}
    finally:
        connection.close()

    get_logger().info("Completed analytics against %s", database_path)
    return results


if __name__ == "__main__":
    run_analytics()
