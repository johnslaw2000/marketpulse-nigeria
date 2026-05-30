from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# DATABASE CONNECTION
def get_db_connection():
    conn = psycopg2.connect(
        dbname="marketpulse",
        user="marketuser",
        password="marketpass",
        host="localhost"
    )
    return conn

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# ADD PRICE
@app.route('/add', methods=['GET', 'POST'])
def add_price():

    if request.method == 'POST':

        item = request.form['item']
        price = request.form['price']
        market = request.form['market']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO prices (item, price, market) VALUES (%s, %s, %s)",
            (item, price, market)
        )

        conn.commit()

        cur.close()
        conn.close()

        return "Price Added Successfully ✅"

    return render_template('add.html')

# VIEW PRICES
@app.route('/prices')
def prices():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM prices")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('prices.html', rows=rows)



@app.route('/delete/<int:id>')
def delete_price(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM prices WHERE id = %s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return "Deleted successfully"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
