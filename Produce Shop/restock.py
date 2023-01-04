import psycopg2
import time
import random

connection = psycopg2.connect("dbname=assignment3 user=postgres password=mypostgresdb")

def displayInventoryTable():
    cursor = connection.cursor()
    sql = "SELECT Inventory.inventory_id, Inventory.product_id, Inventory.stock FROM Inventory ORDER BY Inventory.product_id"
    cursor.execute(sql)

    print("Inventory Table: ")
    for row in cursor:
        print(f"inventory_id: {row[0]}, product_id: {row[1]}, stock: {row[2]}")

# display original contents of table
displayInventoryTable()
print()

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
    # update the stock of a random set of items
    update()
    print()
    
    # commit to the database
    connection.commit()
    
    # display the updated inventory table
    displayInventoryTable()
    print()
    
    time.sleep(5)