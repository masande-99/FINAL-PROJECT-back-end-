import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message


def init_sqlite_db():
    conn = sqlite3.connect('products.db')
    print("Opened database successfully")

    conn.execute(
        'CREATE TABLE IF NOT EXISTS items (product_name TEXT, brand_name TEXT, available_sizes TEXT, price TEXT,images TEXT, product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_image TEXT)')
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
mail= Mail(app)
CORS(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gontyelenimasande@gmail.com'
app.config['MAIL_PASSWORD'] = 'Sandei99#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

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
            image = request.form['image']

            with sqlite3.connect('products.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO items (product_name, brand_name, available_sizes , product_id, product_image) VALUES (?,?, ?, ?, ?)",
                    (p_name, b_name, size, id, image))
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


@app.route('/contact-us/',methods=['GET','POST'])
def contact_us():
    if request.method == "POST":
        try:
            p_name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            comment = request.form['comments']


            with sqlite3.connect('products.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO logins (fullname, email, username, comments) VALUES (?,?, ?, ?)",
                            (p_name, email, username, comment))
                con.commit()
                # send_email(p_name,email,username,comment)
                test_sending_mail()
                msg = "Item added successfully."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation or while sending the email: " + str(e)

        finally:
            con.close()
            return jsonify(msg)


def test_sending_mail():
    from smtplib import SMTP
    server = SMTP('smtp.gmail.com', 587)
    try:
        sender_email = 'gontyelenimasande@gmail.com'
        receiver_email = 'gontyelenimasande@gmail.com'
        password = 'Sandei99#'

        server.starttls()
        server.login(send_email, password)
        server.sendmail(send_email, receiver_email, 'This is a test.')
        print('Message sent succesfully')
    except Exception as e:
        print("Something wrong happened: " + str(e))
    finally:
        server.close()


def send_email(p_name,email,username,comment):
    msg = Message('Hello', sender = 'gontyelenimasande@gmail.com', recipients=['gontyelenimasande@gmail.com'])
    msg.body = f'fullname :{p_name} ' \
               f'email :{email} ' \
               f'username :{username}' \
               f'comment :{comment}'
    mail.send(msg)
    return "Sent"


@app.route('/products/')
def insert_products():
    try:
        with sqlite3.connect('products.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('sneaker', 'Brand :Nike', 'size :6-8\n','Available:  R800', 'https://i.postimg.cc/qMTZDBQn/no3.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Half boot sneaker', 'brand :Converse', 'size :6-8\n','Available:  R1200', 'https://i.postimg.cc/Fztn4h4M/no6.png')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand :Nike', 'size :6-8\n', 'Available:  R600', 'https://i.postimg.cc/V6HmBrXj/istockphot.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Half boot sneaker', 'Brand :jordan', 'Size :7-9\n', 'Available: R2200', 'https://i.postimg.cc/g2wRv8RK/jordan-shoes-1777572-340.png')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Half boot sneaker', 'Brand : Nike', 'size :6-8\n','Available:  R1700', 'https://i.postimg.cc/WprH7qmT/no4.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Air max', 'Brand : Nike', 'size : 7-9\n','Available:  R1185', 'https://i.postimg.cc/4x42Z8Dx/no1.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand', 'size :7-9\n','Available:  R900', 'https://i.postimg.cc/HLwgKvXs/white.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand : Adidas', 'size :7-9\n','Available:  R2175', 'https://i.postimg.cc/ZqS840BF/adidass.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('full boot', 'Brand : Timberland', 'size :7-9\n','Available:  R3120', 'https://i.postimg.cc/K8FSTrC6/no11.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('sneaker', 'Brand : Reebock', 'size : 7-9\n','Available:  R1280', 'https://i.postimg.cc/MHh3zq8k/reebok-2061623-340.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand : Prada', 'size : 7-9\n','Available:  R1840', 'https://i.postimg.cc/1tMcWPz0/black-1868865-340.jpg')")
            cur.execute("INSERT INTO items(product_name, brand_name, available_sizes, price, images) VALUES('Sneaker', 'Brand : Adidas', 'size :7-9\n','Available:  R2180', 'https://i.postimg.cc/W39gGn9X/adidas-2554690-340.png')")
            con.commit()
            msg= 'Record successfully added.'
    except Exception as e:
        con.rollback()
        msg = 'Error occurred in insert operation'+str(e)
    finally:
        con.close()
    return jsonify(msg)

@app.route('/show-products/', methods= ['GET'])
def show_products():
    data = []
    try:
        with sqlite3.connect('products.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * FROM items')
            data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching products from the database")
    finally:
        con.close()
        return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
