import psycopg2

connection = psycopg2.connect("dbname=assignment3 user=postgres password=mypostgresdb")
drop_cursor = connection.cursor()

drop_cursor.execute("DROP TABLE Customer")
print("Customer table dropped successfully")

drop_cursor.execute("DROP TABLE Products")
print("Products table dropped successfully")

drop_cursor.execute("DROP TABLE Orders")
print("Orders table dropped successfully")

drop_cursor.execute("DROP TABLE Payment")
print("Payment table dropped successfully")

drop_cursor.execute("DROP TABLE Inventory")
print("Inventory table dropped successfully")

connection.commit()