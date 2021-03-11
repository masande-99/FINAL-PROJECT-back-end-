import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


# A function to create a database and tables
def init_sqlite_db():
    conn = sqlite3.connect('products.db')
    print("Opened database successfully")

    conn.execute(
        'CREATE TABLE IF NOT EXISTS items (product_name TEXT, brand_name TEXT, available_sizes TEXT, price TEXT,images TEXT, product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)')
    print("Table(items) created successfully")
    conn.execute(
        'CREATE TABLE IF NOT EXISTS users(fullname TEXT, email TEXT, username TEXT, password TEXT, address TEXT )')
    print("Table(users) created successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS logins(fullname TEXT, email TEXT, username TEXT,  comments TEXT)')
    print("Table(login) created successfully")
    conn.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


init_sqlite_db()

app = Flask(__name__)
CORS(app)


# A route to add a new item to the database from the front-end
@app.route('/')

@app.route('/add-new-item/', methods=['POST'])
def add_new_item():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            p_name = post_data['name']
            b_name = post_data['brand']
            size = post_data['size']
            id = post_data['id']
            image = post_data['image']

            with sqlite3.connect('products.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO items (product_name, brand_name, available_sizes , product_id,images) VALUES (?,?, ?, ?, ?)",
                    (p_name, b_name, size, id, image))
                con.commit()
                msg = "Item added successfully."
        except Exception as e:
            con.rollback()
            msg = ("Error occurred in insert operation: " + str(e))

        finally:
            con.close()
            return jsonify(msg)


# A route to fetch items/products from the data base



# A route to register a new user to the database
@app.route('/add-new-user/', methods=['POST'])
def add_new_user():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            p_name = post_data['name']
            email = post_data['email']
            username = post_data['username']
            password = post_data['password']
            address = post_data['address']
            with sqlite3.connect('products.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (fullname, email, username, password , address) VALUES (?,?, ?, ?, ?)",
                            (p_name, email, username, address, password))
                con.commit()
                msg = "Item added successfully."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)


# A route to fetch all the users from the database
@app.route('/show-users/', methods=["GET"])
def show_users():
    global records
    records = []
    try:
        with sqlite3.connect('products.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records)

# A route that adds products to the database from the back end
@app.route('/products/')
def insert_products():
    try:
        with sqlite3.connect('products.db') as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('sneaker', 'Brand :Nike', 'size :6-8\n','Available:  R800', 'https://i.postimg.cc/qMTZDBQn/no3.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Half boot sneaker', 'brand :Converse', 'size :6-8\n','Available:  R1200', 'https://i.postimg.cc/Fztn4h4M/no6.png')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand :Nike', 'size :6-8\n', 'Available:  R600', 'https://i.postimg.cc/V6HmBrXj/istockphot.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Half boot sneaker', 'Brand :jordan', 'Size :7-9\n', 'Available: R2200', 'https://i.postimg.cc/g2wRv8RK/jordan-shoes-1777572-340.png')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Half boot sneaker', 'Brand : Nike', 'size :6-8\n','Available:  R1700', 'https://i.postimg.cc/WprH7qmT/no4.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Air max', 'Brand : Nike', 'size : 7-9\n','Available:  R1185', 'https://i.postimg.cc/4x42Z8Dx/no1.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand', 'size :7-9\n','Available:  R900', 'https://i.postimg.cc/HLwgKvXs/white.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand : Adidas', 'size :7-9\n','Available:  R2175', 'https://i.postimg.cc/ZqS840BF/adidass.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('full boot', 'Brand : Timberland', 'size :7-9\n','Available:  R3120', 'https://i.postimg.cc/K8FSTrC6/no11.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('sneaker', 'Brand : Reebock', 'size : 7-9\n','Available:  R1280', 'https://i.postimg.cc/MHh3zq8k/reebok-2061623-340.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand : Prada', 'size : 7-9\n','Available:  R1840', 'https://i.postimg.cc/1tMcWPz0/black-1868865-340.jpg')")
            cur.execute(
                "INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand : Adidas', 'size :7-9\n','Available:  R2180', 'https://i.postimg.cc/W39gGn9X/adidas-2554690-340.png')")
            con.commit()
            msg = 'Record successfully added.'
    except Exception as e:
        con.rollback()
        msg = 'Error occurred in insert operation' + str(e)
    finally:
        con.close()
    return jsonify(msg)


if __name__ == '__main__':
    app.run(debug=True)
