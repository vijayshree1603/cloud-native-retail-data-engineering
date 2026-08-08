-- 1. Total Revenue
SELECT
    SUM(total_amount) AS total_revenue
FROM retail_sales;


-- 2. Revenue by Category
SELECT
    category,
    SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY category
ORDER BY revenue DESC;


-- 3. Revenue by Region
SELECT
    region,
    SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY region
ORDER BY revenue DESC;


-- 4. Total Quantity Sold
SELECT
    SUM(quantity) AS total_quantity
FROM retail_sales;


-- 5. Average Order Value
SELECT
    AVG(total_amount) AS average_order_value
FROM retail_sales;


-- 6. Highest Value Orders
SELECT
    order_id,
    customer_id,
    category,
    total_amount
FROM retail_sales
ORDER BY total_amount DESC
LIMIT 5;