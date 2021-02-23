import sqlite3
from flask import Flask, render_template, request

def init_sqlite_db():
    conn = sqlite3.connect('mydatabase.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS items (product-name TEXT, brand-name TEXT, available-sizes TEXT, pin TEXT)')
    print("Table created successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS orders (productId TEXT, productname TEXT, productphoto TEXT, availablesizes TEXT)')
    print("Table created successfully")
    conn.close()

    init_sqlite_db()

app = Flask(__name__)

@app.route('/')
@app.route('/enter-new/')
def enter_new_student():
    return render_template('index.html')


def convertToBinaryData(billie):
    with open(billie, 'rb') as file:
        blobData = file.read()
    return blobData

#def insertBLOB(productId, productname, productphoto, availablesizes):
    # try:
        #sqliteConnection = sqlite3.connect('mydatabase.db')
        #cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")
        #sqlite_insert_blob_query = """ INSERT INTO items
#                                  (productId, productname, productphoto, availablesizes) VALUES (?, ?, ?, ?)"""
#        empPhoto = convertToBinaryData(productphoto)
#        data_tuple = (productId, productname, productphoto, availablesizes)
#        cursor.execute(sqlite_insert_blob_query, data_tuple)
#        sqliteConnection.commit()
#        print("Image and file inserted successfully as a BLOB into a table")
 #       cursor.close()

#     except sqlite3.Error as error:
#        print("Failed to insert blob data into sqlite table", error)
#     finally:
#        if (sqliteConnection):
#            sqliteConnection.close()
 #           print("the sqlite connection is closed")

#     insertBLOB(1, "Smith", "E:\pynative\Python\photos\smith.jpg", "E:\pynative\Python\photos\smith_resume.txt")
 #    insertBLOB(2, "David", "E:\pynative\Python\photos\david.jpg", "E:\pynative\Python\photos\david_resume.txt")



@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('mydatabase.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM items")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return render_template('index.html', records=records)

app.run(debug=True)
