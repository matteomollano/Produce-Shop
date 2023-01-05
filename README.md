# Produce-Shop

In this project, an arbitrary amount of random customers are created. Each of these customers places an order, with each order 
containing 1-3 random products. The orders are stored in a database using PostgreSQL.

Produce Shop/shop.py:
- Generates 5 tables (Customer, Products, Orders, Payment, and Inventory) to keep track of customer data, store products, order history, payment
information, and product stock
- Adds products to the Products table and initializes the stock of the products in the Inventory table
- Creates customers with randomly generated names using the names module in python
- Places an order for each randomly created customer (each customer has their own randomly generated credit card number, and each order has its own
randomly generated order number)
- Provides functions to display the Customer, Products, Orders, Payment, and Inventory Tables

Produce Shop/revenue_report.py:
- Represents the revenue report of the produce shop
- Displays the name of each product sold, followed by its corresponding quantity sold and revenue earned
- Orders the report in total revenue descending (products with greatest revenue earned to least revenue earned)

Produce Shop/restock.py:
- Runs indefinitely and periodically
- Adds a random amount (1-50) of stock to a random set of products (1 to the length of the inventory table)

Produce Shop/drop_tables.py:
- Used to reset the database and start with a new simulation
