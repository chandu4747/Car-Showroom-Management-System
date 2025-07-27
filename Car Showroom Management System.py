from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('showroom.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            brand TEXT NOT NULL,
            price INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        model = request.form['model']
        brand = request.form['brand']
        price = request.form['price']

        conn = sqlite3.connect('showroom.db')
        c = conn.cursor()
        c.execute("INSERT INTO cars (model, brand, price) VALUES (?, ?, ?)", (model, brand, price))
        conn.commit()
        conn.close()
        return redirect('/view')
    return render_template('add_car.html')

@app.route('/view')
def view_cars():
    conn = sqlite3.connect('showroom.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars WHERE status='Available'")
    cars = c.fetchall()
    conn.close()
    return render_template('view_cars.html', cars=cars)

@app.route('/sold')
def sold_cars():
    conn = sqlite3.connect('showroom.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars WHERE status='Sold'")
    cars = c.fetchall()
    conn.close()
    return render_template('sold_cars.html', cars=cars)

@app.route('/sell/<int:car_id>')
def sell_car(car_id):
    conn = sqlite3.connect('showroom.db')
    c = conn.cursor()
    c.execute("UPDATE cars SET status='Sold' WHERE id=?", (car_id,))
    conn.commit()
    conn.close()
    return redirect('/view')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
