import sqlite3
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('products.db')
    conn.cursor()
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS items (product_name TEXT, brand_name TEXT, available_sizes TEXT, product_id TEXT, product_image TEXT)')
    print("Table(items) created successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users(fullname TEXT, username TEXT, password TEXT, usernameId TEXT)')
    print("Table(users) created successfully")
    conn.close()

    init_sqlite_db()


app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]] =row[idx]


@app.route('/')
@app.route('/enter-new-item/')
def enter_new_item():
    return render_template('product.html')


@app.route('/add-new-item/', methods=['POST'])
def add_new_item():
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
            msg = "Error occurred in insert operation: " + e

        finally:
            con.close()
            return render_template('items.html', msg=msg)


@app.route('/show-items/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('products.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM items")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records=records)



