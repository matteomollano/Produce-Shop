import psycopg2
import time

connection = psycopg2.connect("dbname=assignment3 user=postgres password=mypostgresdb")

while True:
    print("Revenue Report")
    report_cursor = connection.cursor()
    report_sql = '''SELECT product_name, SUM(quantity) as quantity_sold, SUM(total_price_in_usd) as total_revenue FROM Orders
    JOIN Products on Products.product_id = Orders.product_id GROUP BY product_name ORDER BY total_revenue DESC, quantity_sold DESC, product_name'''
    report_cursor.execute(report_sql)

    for report in report_cursor:
        print(f"{report[0]} sold {report[1]} total rev ${report[2]}")
    
    print()
    time.sleep(1)