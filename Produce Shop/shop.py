import psycopg2
import random
import names
import time

connection = psycopg2.connect("dbname=assignment3 user=postgres password=mypostgresdb")

# create the Customer table
customer_cursor = connection.cursor()
sql = '''CREATE TABLE IF NOT EXISTS Customer(
   customer_id SERIAL NOT NULL PRIMARY KEY,
   customer_name VARCHAR(200) NOT NULL
)'''
customer_cursor.execute(sql)
##print("Customer table created successfully")

# create the Products table
product_cursor = connection.cursor()
sql2 = '''CREATE TABLE IF NOT EXISTS Products(
    product_id SERIAL NOT NULL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    product_price_in_usd DECIMAL(12,2) NOT NULL
)'''
product_cursor.execute(sql2)
##print("Products table created successfully")

# create the Orders Table
order_cursor = connection.cursor()
sql3 = '''CREATE TABLE IF NOT EXISTS Orders(
    id SERIAL NOT NULL PRIMARY KEY,
    order_id_number VARCHAR(20) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price_in_usd DECIMAL(12,2) NOT NULL
)'''
order_cursor.execute(sql3)
##print("Orders table created successfully")

# create the Payment table
payment_cursor = connection.cursor()
sql4 = '''CREATE TABLE IF NOT EXISTS Payment(
    payment_id SERIAL NOT NULL PRIMARY KEY,
    customer_id INT NOT NULL,
    credit_card_number VARCHAR(19) NOT NULL
)'''
payment_cursor.execute(sql4)
##print("Payment table created successfully")

# create the Inventory Table (added for assignment 5)
inventory_cursor = connection.cursor()
inventory_sql = '''CREATE TABLE IF NOT EXISTS Inventory(
    inventory_id SERIAL NOT NULL PRIMARY KEY,
    product_id INT NOT NULL,
    stock INT NOT NULL
)'''
inventory_cursor.execute(inventory_sql)
##print("Inventory table created successfully")

# insert items into Products table
insert_cursor = connection.cursor()
insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('apple', 0.25)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('pear', 0.76)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('orange', 0.85)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('watermelon', 6.99)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('bunch of bananas', 1.69)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('bag of clementines', 3.98)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('bag of baby carrots', 1.48)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('pack of strawberries', 2.51)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('pack of raspberries', 2.24)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('pack of blackberries', 2.24)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('pack of blueberries', 2.24)'''
insert_cursor.execute(insert_sql)

insert_sql = '''INSERT INTO Products(product_name, product_price_in_usd) VALUES ('pack of grapes', 4.99)'''
insert_cursor.execute(insert_sql)

# print the Product table
select_cursor = connection.cursor()
product_sql = "SELECT Products.product_id, Products.product_name, Products.product_price_in_usd FROM Products"
select_cursor.execute(product_sql)

print("Products Table: ")
for product in select_cursor:
    print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
print()

## added for assignment 5 ##
# add stock for each item to the inventory table
def initializeStock():
    cursor = connection.cursor()
    sql = "SELECT count(*) FROM Products"
    cursor.execute(sql)
    
    global num_products
    for row in cursor:
        num_products = row[0]
    
    for i in range(1, num_products + 1):
        cursor.execute(f"INSERT INTO Inventory(product_id, stock) VALUES ({i}, 5)")
initializeStock()

# print the Inventory table
display_inv_cursor = connection.cursor()
sql = "SELECT Inventory.inventory_id, Inventory.product_id, Inventory.stock FROM Inventory ORDER BY Inventory.product_id"
display_inv_cursor.execute(sql)

print("Inventory Table: ")
for row in display_inv_cursor:
    print(f"inventory_id: {row[0]}, product_id: {row[1]}, stock: {row[2]}")
print()
        
## create the list of available products (products with a stock > 0)
def availableProducts():
    cursor = connection.cursor()
    cursor.execute("SELECT product_id, stock FROM Inventory")
    
    array = []
    for row in cursor:
        if row[1] > 0:
            array.append(row[0])
    
    return array
    
def randomNum():
    return random.randint(1,3)

def randomQuantity():
    ## I didn't want to use 1 to 1000 since when is someone going to buy 1000 produce items?
    ## but if you want 1000 items, you can simply change the following line to
    ## return random.randint(1,1000)
    return random.randint(1,5)

def randomCCN():
    number = random.randint(0,9)
    credit_card_number = ""
    
    for i in range(16):
        credit_card_number += str(number)
        if (len(credit_card_number) - credit_card_number.count(' ')) % 4 == 0:
            credit_card_number += " "
        number = random.randint(0,9)
    ## to remove the extra space added to the end of the credit card number
    credit_card_number = credit_card_number.rstrip()
    return credit_card_number

def randomOrderNumber():
    number = random.randint(0,9)
    order_number = "#"
    for i in range(17):
        order_number += str(number)
        if len(order_number) == 4 or len(order_number) == 12:
            order_number += "-"
        number = random.randint(0,9)
    return order_number

def addCustomer(name):
    ## insert the customer's name into the Customer table
    cursor = connection.cursor()
    sql = f"INSERT INTO Customer(customer_name) VALUES ('{name}')"
    cursor.execute(sql)
    #print(f"{name} added to the Customer table successfully")
    
    ## add a random credit card number for each customer to the Payment Table
    customer_id = getCustomerID(name)
    ccn = randomCCN()
    sql = f"INSERT INTO Payment(customer_id, credit_card_number) VALUES ( {customer_id} , '{ccn}' )"
    cursor.execute(sql)
    
def getCustomerID(name):
    # selecting the customer id and customer name for each record in the Customer table
    cursor = connection.cursor()
    sql = "SELECT customer_id, customer_name FROM Customer"
    cursor.execute(sql)
    
    ## getting the customer id for a specific customer
    customer_id = 0
    for customer in cursor:
        if customer[1] == name:
            customer_id = customer[0]
    return customer_id

def addOrder(name):
    # generate a random order id number
    order_id_number = randomOrderNumber()
    # get a random number of products for the order
    number_of_products = randomNum()
    # get the customer_id of the customer we are adding an order for
    customer_id = getCustomerID(name)
    
    select_cursor = connection.cursor()
    insert_cursor = connection.cursor()
    update_cursor = connection.cursor()
    stock_cursor = connection.cursor()
    
    # get the product id and price for each of the products that will be added to the Orders table for that given customer
    for i in range(number_of_products):
        
        ## array used to get an available item for the order
        available_stock_array = availableProducts()
        
        ## if there are no products available for purchase, then do not place an order
        if len(available_stock_array) == 0:
            print("No products are available for purchase at this time\n")
            break
        
        # choose a random product from the available stock array
        product_id = random.choice(available_stock_array)
        
        ## get the cost of the random available product
        sql = f"SELECT product_price_in_usd FROM Products WHERE Products.product_id = {product_id}"
        select_cursor.execute(sql)
        
         # get a random quantity for each product
        quantity = randomQuantity()
        
        ## check to see if there is enough available stock for the random product
        sql = f"SELECT stock FROM Inventory WHERE Inventory.product_id = {product_id}"
        stock_cursor.execute(sql)
        
        global stock
        for row in stock_cursor:
            stock = row[0]
        
        # if the quantity trying to be purchased is more than the current stock of this product, 
        # do not update the inventory table AND do not order the product
        # go to the next iteration of the for loop for any subsequent random product that a customer attempts to purchase
        if (quantity > stock):
            print(f"Sorry there isn't enough stock to purchase product {product_id}")
            print(f"You tried to purchase {quantity} products, while the available stock is {stock}\n")
            continue
        
        # update the stock for a given amount based on how many of that item were purchased
        sql = f"UPDATE Inventory SET stock = stock - {quantity} WHERE Inventory.product_id = {product_id}"
        update_cursor.execute(sql)
        
        # get the product price of the randomly selected product
        global price_of_product
        for product in select_cursor:
            price_of_product = product[0]
        total_price_in_usd = price_of_product * quantity
    
        ## add the order to the Orders table
        insert_sql = f'''INSERT INTO Orders(order_id_number, customer_id, product_id, quantity, total_price_in_usd) 
        VALUES ('{order_id_number}', {customer_id}, {product_id}, {quantity}, {total_price_in_usd})'''
        insert_cursor.execute(insert_sql)

## Displaying the tables    
def displayCustomerTable():
    cursor = connection.cursor()
    sql = "SELECT customer_id, customer_name FROM Customer"
    cursor.execute(sql)
    
    print("Customer Table: ")
    for customer in cursor:
        print(f"customer_id: {customer[0]}, customer_name: {customer[1]}")
        
def displayProductTable():
    cursor = connection.cursor()
    product_sql = "SELECT Products.product_id, Products.product_name, Products.product_price_in_usd FROM Products"
    cursor.execute(product_sql)

    print("Products Table: ")
    for product in cursor:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
           
def displayOrderTable():
    cursor = connection.cursor()
    sql = "SELECT id, order_id_number, order_date, customer_id, product_id, quantity, total_price_in_usd FROM Orders"
    cursor.execute(sql)
    
    print("Order Table: ")
    for order in cursor:
        print(f"order_id: {order[0]}, order_id_number: {order[1]}, order_date: {order[2]}, customer_id: {order[3]}, product_id: {order[4]}, quantity: {order[5]}, total_price_in_usd: {order[6]}")

def displayPaymentTable():
    ## displaying the Payment table
    cursor = connection.cursor()
    sql = "SELECT payment_id, customer_id, credit_card_number FROM Payment"
    cursor.execute(sql)

    print("Payment Table: ")
    for payment in cursor:
        print(f"payment_id: {payment[0]}, customer_id: {payment[1]}, ccn: {payment[2]}")

# added for assignment 5
def displayInventoryTable():
    cursor = connection.cursor()
    sql = "SELECT Inventory.inventory_id, Inventory.product_id, Inventory.stock FROM Inventory ORDER BY Inventory.product_id"
    cursor.execute(sql)

    print("Inventory Table: ")
    for row in cursor:
        print(f"inventory_id: {row[0]}, product_id: {row[1]}, stock: {row[2]}")

# function for assignment 5 (also found in assignment5.py)
# adds a random amount of stock to a random set of products
def update():
    cursor = connection.cursor()
    sql = "SELECT count(*) FROM Inventory"
    cursor.execute(sql)
    
    inv_length = cursor.fetchone()[0]
    
    # number of products to update
    num_of_products = random.randint(1, inv_length)
    
    print("Restock: ")
    for i in range(num_of_products):
        # amount of stock to add to each product
        random_amount = random.randint(1, 50)
        
        # random product to add the random stock to
        random_product = random.randint(1, inv_length)
        
        print(f"product_id {random_product} += stock of {random_amount}")

        # update the stock in the inventory table for the random product
        sql = f"UPDATE Inventory SET stock = stock + {random_amount} WHERE Inventory.product_id = {random_product}"
        cursor.execute(sql)

while True:
    # generate a random name using the names module
    name = names.get_full_name()
    
    # add this random person to the Customer table
    addCustomer(name)
    
    #update()
    #print()
    
    # show inventory table after update
    #displayInventoryTable()
    #print()
    
    # place an order for this random Customer
    addOrder(name)
    
    displayCustomerTable()
    print()
    
    displayPaymentTable()
    print()
    
    displayOrderTable()
    print()
    
    # show inventory table after order
    #displayInventoryTable()
    #print()
        
    # commit to the database
    connection.commit()
    
    time.sleep(5)