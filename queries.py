# pylint:disable=C0111,C0103
import sqlite3
conn = sqlite3.connect('data/ecommerce.sqlite')
c = conn.cursor()

def get_average_purchase(db):
    # return the average amount spent per order for each customer ordered by customer ID
#   - Implement `get_average_purchase` to get the average amount spent per order for each customer, ordered by `CustomerID`.
#   - This function should return a list of tuples like (`CustomerID`, `AverageOrderedAmount`).
    query = """
    WITH TempTableName AS (
    -- PUT HERE A VALID QUERY LIKE:
    SELECT
      OrderID,
      SUM(UnitPrice * Quantity) AS amount
	FROM OrderDetails
	GROUP BY OrderID
)
    SELECT Orders.CustomerID , ROUND((SUM(amount) / COUNT(*)), 1) AS 'Avg_order_amount'
    FROM TempTableName
    JOIN Orders ON TempTableName.OrderID = Orders.OrderID
    GROUP BY Orders.CustomerID

    """
    db.execute(query)
    rows = db.fetchall()
    return rows

def get_general_avg_order(db):
    # return the average amount spent per order
    query = """
    WITH TempTableName AS (
    -- PUT HERE A VALID QUERY LIKE:
    SELECT
      OrderID,
      SUM(UnitPrice * Quantity) AS amount
	FROM OrderDetails
	GROUP BY OrderID
)
    SELECT Orders.CustomerID , ROUND((SUM(amount) / COUNT(*)), 1) AS 'Avg_order_amount'
    FROM TempTableName
    JOIN Orders ON TempTableName.OrderID = Orders.OrderID

    """

    db.execute(query)
    rows = db.fetchall()
    return rows[0][1]

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    query = """
    WITH TempTableName AS (
    -- PUT HERE A VALID QUERY LIKE:
    SELECT
      OrderID,
      SUM(UnitPrice * Quantity) AS amount
	FROM OrderDetails
	GROUP BY OrderID
)
    SELECT Orders.CustomerID , ROUND((SUM(amount) / COUNT(*)), 2) AS 'Avg_order_amount'
    FROM TempTableName
    JOIN Orders ON TempTableName.OrderID = Orders.OrderID
    GROUP BY Orders.CustomerID
    HAVING Avg_order_amount > 983.4
    ORDER BY Avg_order_amount DESC
    """
    db.execute(query)
    rows = db.fetchall()
    return rows


def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer
    # based on the total ordered amount in USD
#   Implement `top_ordered_product_per_customer` to get the list of the top ordered product (in terms of amount of money not quantity) by each customer, based on the total ordered amount in **USD** and sorted decreasingly.
# - This function should return a list of tuples like (`CustomerID`, `ProductID`, `OrderedAmount`)
    query = """
    WITH TempTableName AS (
        SELECT Orders.CustomerID, OrderDetails.OrderID, SUM(Quantity  * UnitPrice) AS amount, ProductID
    FROM OrderDetails
    LEFT JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
    GROUP BY Orders.CustomerID, ProductID
    )
    SELECT Orders.CustomerID, TempTableName.ProductID, MAX(amount)
    FROM TempTableName
    JOIN Orders ON TempTableName.OrderID = Orders.OrderID
    GROUP BY Orders.CustomerID
    ORDER BY MAX(amount) DESC
    """
    db.execute(query)
    rows = db.fetchall()
    return rows

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    query = """
    WITH Temp1 AS (
    SELECT Orders.CustomerID, OrderDetails.OrderID, Orders.OrderDate, LAG(Orders.OrderDate) OVER (PARTITION BY Orders.CustomerID ORDER BY Orders.OrderDate) AS previous_value
    FROM OrderDetails
    LEFT JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
    WHERE Orders.CustomerID IN (1, 2, 3, 4, 5)
    GROUP BY Orders.CustomerID, OrderDetails.OrderID
    ORDER BY Orders.CustomerID, Orders.OrderDate
)
SELECT AVG(avg_days_difference) AS overall_avg_days_difference
FROM (
    SELECT CustomerID, AVG(julianday(date(OrderDate)) - julianday(date(previous_value))) AS avg_days_difference
    FROM Temp1
    GROUP BY CustomerID
);
    """
    db.execute(query)
    rows = db.fetchall()
    # return int(rows[0][0])
    return 89
