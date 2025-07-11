# 文件：app.py
from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
from decimal import Decimal, InvalidOperation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=RestaurantDB;"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str)
    return conn, conn.cursor()

def fetchall_dict(cursor):
    cols = [col[0] for col in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def fetchone_dict(cursor):
    row = cursor.fetchone()
    if not row:
        return None
    cols = [col[0] for col in cursor.description]
    return dict(zip(cols, row))


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn, cursor = get_db_connection()
        cursor.execute(
            "SELECT id, username FROM users WHERE username=? AND password=?",
            username, password
        )
        user = fetchone_dict(cursor)
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['cart'] = {}
            return redirect(url_for('order'))
        else:
            error = '用户名或密码错误'
    return render_template('login.html', error=error)


@app.route('/order')
def order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn, cursor = get_db_connection()
    cursor.execute("SELECT id, name, price FROM Menu")
    items = fetchall_dict(cursor)
    conn.close()
    return render_template('order.html', items=items)


@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('order'))


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn, cursor = get_db_connection()
    cart_data = session.get('cart', {})
    items = []
    total = Decimal('0')
    for item_id, qty in cart_data.items():
        cursor.execute("SELECT id, name, price FROM Menu WHERE id=?", item_id)
        row = cursor.fetchone()
        if row:
            item = {'id': row[0], 'name': row[1], 'price': Decimal(str(row[2]))}
            item['quantity'] = qty
            item['subtotal'] = item['price'] * qty
            total += item['subtotal']
            items.append(item)
    conn.close()
    return render_template('cart.html', items=items, total=total)


@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    new_cart = {}
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            item_id = key.split('_', 1)[1]
            try:
                qty = int(value)
                if qty > 0:
                    new_cart[item_id] = qty
            except ValueError:
                pass
    session['cart'] = new_cart
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn, cursor = get_db_connection()

    if request.method == 'POST':
        raw = request.form.get('discount', '').strip()
        try:
            discount = Decimal(raw) if raw else Decimal('1.0')
        except (InvalidOperation, TypeError):
            discount = Decimal('1.0')

        total = Decimal('0')
        for item_id, qty in session.get('cart', {}).items():
            cursor.execute("SELECT price FROM Menu WHERE id=?", item_id)
            price = Decimal(str(cursor.fetchone()[0]))
            total += price * qty

        final_price = (total * discount).quantize(Decimal('0.01'))

        cursor.execute(
            """
            INSERT INTO Orders
              (customer_name, total, discount, final_price, created_at)
            VALUES
              (?, ?, ?, ?, GETDATE())
            """,
            session['username'],
            total,
            discount,
            final_price
        )
        order_id = cursor.execute("SELECT @@IDENTITY").fetchval()

        for item_id, qty in session.get('cart', {}).items():
            cursor.execute(
                "INSERT INTO OrderItems (order_id, menu_item_id, quantity) VALUES (?, ?, ?)",
                order_id, item_id, qty
            )

        conn.commit()
        conn.close()
        session['cart'] = {}
        return redirect(url_for('result', order_id=order_id))

    items = []
    total = Decimal('0')
    for item_id, qty in session.get('cart', {}).items():
        cursor.execute("SELECT id, name, price FROM Menu WHERE id=?", item_id)
        row = cursor.fetchone()
        if row:
            item = {'id': row[0], 'name': row[1], 'price': Decimal(str(row[2]))}
            item['quantity'] = qty
            item['subtotal'] = item['price'] * qty
            total += item['subtotal']
            items.append(item)
    conn.close()
    return render_template('checkout.html', items=items, total=total)


@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    order_id = request.args.get('order_id')
    return render_template('result.html', order_id=order_id)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn, cursor = get_db_connection()
    cursor.execute(
        "SELECT id, customer_name, total, discount, final_price, created_at "
        "FROM Orders WHERE customer_name=? ORDER BY created_at DESC",
        session['username']
    )
    orders = fetchall_dict(cursor)
    for o in orders:
        cursor.execute(
            """
            SELECT oi.menu_item_id AS item_id, m.name, m.price, oi.quantity
            FROM OrderItems oi
            JOIN Menu m ON oi.menu_item_id=m.id
            WHERE oi.order_id=?
            """,
            o['id']
        )
        details = fetchall_dict(cursor)
        # 将价格类型转换为 Decimal
        for d in details:
            d['price'] = Decimal(str(d['price']))
        o['order_items'] = details  # 重命名字段
    conn.close()
    return render_template('history.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)
