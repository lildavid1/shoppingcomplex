# from cs50 import SQL
# from werkzeug.security import check_password_hash, generate_password_hash

# db = SQL("sqlite:///project.db")

# rows = db.execute("SELECT * FROM products")

# print(rows)

# title = input("title: ")

# img = input("img: ")

# desc = input("desc: ")

# name = input("name: ")

# price = input("price: ")

# db.execute("INSERT INTO products (title,img,desc,name,price) VALUES(?,?,?,?,?)", title,img,desc,name,price)

# rows = db.execute("SELECT * FROM 'products'")

# print(rows)
sum = 0

arr = [9, 2, 7, 4, 5, 6, 8, 3]

def index():
    sum = 0
    arr = [9, 2, 7, 4, 5, 6, 8, 3] 
    for num in arr:

        if num % 2 == 0:
            sum = sum+num

    print(sum)

index()