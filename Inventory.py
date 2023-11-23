import sqlite3 as sql

# Connecting DB and creating cursor
con = sql.connect('inventory.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS items(item, type, quantity, unit, price_per_unit)")

# Initializing some data
# cur.execute("""
#     INSERT INTO items VALUES
#             ('Lettuce', 'Produce', 15, 'Heads', 0.50),
#             ('Beef', 'Meat', 8, 'Cases', 13.50)
# """)

# Function to display all items in inventory
def displayItems(array):
    print()
    for i in array:
        print(f'{i[0]}, {i[1]}. Currently {i[2]} {i[3]} on hand at ${i[4]} per unit.')
    print()

# Function to select specific item in inventory
def selectItem():
    displayItems(item_array)
    global item
    item = input("Select one item: ")
    
    global available 
    available = cur.execute(f"SELECT quantity FROM items WHERE item='{item}'").fetchone()[0]
    
    global unit
    unit = cur.execute(f"SELECT unit FROM items WHERE item='{item}'").fetchone()[0]
    
    global price
    price = cur.execute(f"SELECT price_per_unit FROM items WHERE item='{item}'").fetchone()[0]

# Loops menu
while True:
    # Save previous changes
    con.commit()
    cur.execute("SELECT * FROM items")
    item_array = cur.fetchall()
    print(f'''\nMenu: 
        1. Sell Item: 
        2. Order Item: 
        3. Add Item: 
        4. Remove Item:
        5. View Items: 
        6. Quit''')
    action = input('Please Choose One Option: ')

    # Selling Item from Inventory
    if action == '1':
        selectItem()
        quant = int(input(f"How many of {available} {unit.lower()} were sold? "))
        
        if quant > available:
            print("Not enough available to sell this amount.")
        else:
            cur.execute(f"UPDATE items SET quantity = {available-quant} WHERE item='{item}'")
            print(f'{quant} sold for {price*quant}')
            input(f'Now {available-quant} remaining')
    
    # Ordering item to inventory
    if action == '2':
        selectItem()
        quant = int(input(f"How many {unit.lower()} are needed? "))
        cur.execute(f"UPDATE items SET quantity = {available+quant} WHERE item='{item}'")
        print(f'{quant} purchased for ${price*quant}')
        input(f'Now {available+quant} available')

    # Adding new item to inventory
    if action == '3':
        newItem = input("Name of the item: ")
        newType = input("Type of item: ")
        newQuantity = input("Quantity on hand: ")
        newUnit = input('Units of item: ')
        newPrice = input('Unit price: ')

        cur.execute(f"INSERT INTO items VALUES ('{newItem}', '{newType}', {newQuantity}, '{newUnit}', {newPrice})")
        input('Item added.')

    # Removing item from inventory
    if action == '4':
        selectItem()
        cur.execute(f"DELETE FROM items WHERE item='{item}'")
        input('Item Deleted.')

    # View available items
    if action == '5':
        displayItems(item_array)
        input()

    # Quit inventory
    if action == '6':
        break

# Saving and closing db objects
con.commit()
cur.close()
con.close()