import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('products.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS items (product_name TEXT, brand_name TEXT, available_sizes TEXT, product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_image TEXT)')
    print("Table(items) created successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users(fullname TEXT, email TEXT, username TEXT, password TEXT, address TEXT )')
    print("Table(users) created successfully")
    conn.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
init_sqlite_db()


app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/enter-new-item/')
def enter_new_item():
    return render_template('product.html')


@app.route('/add-new-item/', methods=['POST'])
def add_new_item():
    msg = None
    if request.method == "POST":
        try:
            p_name = request.form['name']
            b_name = request.form['brand']
            size = request.form['size']
            id = request.form['id']
            image =request.form['image']

            with sqlite3.connect('products.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO items (product_name, brand_name, available_sizes , product_id, product_image) VALUES (?,?, ?, ?, ?)", (p_name, b_name, size, id, image))
                con.commit()
                msg = "Item added successfully."
        except Exception as e:
            con.rollback()
            msg = ("Error occurred in insert operation: " + str(e))

        finally:
            con.close()
            return jsonify(msg)


@app.route('/show-items/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('products.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM items")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)


@app.route('/add-new-user/', methods=['POST'])
def add_new_user():
    msg = None
    if request.method == "POST":
        try:
            p_name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            address = request.form['address']
            password = request.form['password']

            with sqlite3.connect('products.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (fullname, email, username, password , address) VALUES (?,?, ?, ?, ?)", (p_name, email, username, address,password))
                con.commit()
                msg = "Item added successfully."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-users/', methods=["GET"])
def show_users():
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


@app.route('/login/', methods=["GET"])
def login(massage=None):
    try:
        p_name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        address = request.form['address']
        password = request.form['password']

        with sqlite3.connect('products.db') as con:
            con.row_factory =dict_factory
            cur = con.cursor()
            cur.execute("SELECT ('email', 'username', 'password') FROM users WHERE email LIKE 'email', WHERE username LIKE 'username%';WHERE password LIKE 'password'")
    except Exception as e:
        con.rollback()
        print("There was an error fetching data from table" + str(e))
    finally:
        con.close()
        return jsonify(msg=massage)





if __name__=='__main__':
    app.run(debug=True)

