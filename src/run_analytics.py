import sqlite3

DATABASE_PATH = "data/retail_sales.db"


def run_query(connection, title, query):
    print(f"\n{'=' * 50}")
    print(title)
    print('=' * 50)

    cursor = connection.execute(query)

    columns = [description[0] for description in cursor.description]
    print(columns)

    for row in cursor.fetchall():
        print(row)


def main():
    connection = sqlite3.connect(DATABASE_PATH)

    # 1. Total Revenue
    run_query(
        connection,
        "1. Total Revenue",
        """
        SELECT SUM(total_amount) AS total_revenue
        FROM retail_sales;
        """
    )

    # 2. Revenue by Category
    run_query(
        connection,
        "2. Revenue by Category",
        """
        SELECT
            category,
            SUM(total_amount) AS revenue
        FROM retail_sales
        GROUP BY category
        ORDER BY revenue DESC;
        """
    )

    # 3. Revenue by Region
    run_query(
        connection,
        "3. Revenue by Region",
        """
        SELECT
            region,
            SUM(total_amount) AS revenue
        FROM retail_sales
        GROUP BY region
        ORDER BY revenue DESC;
        """
    )

    # 4. Total Quantity Sold
    run_query(
        connection,
        "4. Total Quantity Sold",
        """
        SELECT SUM(quantity) AS total_quantity
        FROM retail_sales;
        """
    )

    # 5. Average Order Value
    run_query(
        connection,
        "5. Average Order Value",
        """
        SELECT AVG(total_amount) AS average_order_value
        FROM retail_sales;
        """
    )

    # 6. Highest Value Orders
    run_query(
        connection,
        "6. Highest Value Orders",
        """
        SELECT
            order_id,
            customer_id,
            category,
            total_amount
        FROM retail_sales
        ORDER BY total_amount DESC
        LIMIT 5;
        """
    )

    connection.close()


if __name__ == "__main__":
    main()