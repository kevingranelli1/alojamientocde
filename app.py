from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla de reservas
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departamento TEXT NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            falta_pagar TEXT NOT NULL,
            medio_pago TEXT NOT NULL,
            fecha_ingreso TEXT NOT NULL,
            fecha_egreso TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            mascota TEXT NOT NULL,
            primera_vez TEXT NOT NULL,
            observaciones TEXT
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    reservas = conn.execute('SELECT * FROM reservas').fetchall()
    conn.close()
    return render_template('index.html', reservas=reservas)

@app.route('/crear', methods=('GET', 'POST'))
def crear():
    if request.method == 'POST':
        departamento = request.form['departamento']
        nombre = request.form['nombre']
        precio = request.form['precio']
        falta_pagar = request.form['falta_pagar']
        medio_pago = request.form['medio_pago']
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_egreso = request.form['fecha_egreso']
        telefono = request.form['telefono']
        email = request.form['email']
        mascota = request.form['mascota']
        primera_vez = request.form['primera_vez']
        observaciones = request.form['observaciones']

        conn = get_db_connection()
        conn.execute('INSERT INTO reservas (departamento, nombre, precio, falta_pagar, medio_pago, fecha_ingreso, fecha_egreso, telefono, email, mascota, primera_vez, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (departamento, nombre, precio, falta_pagar, medio_pago, fecha_ingreso, fecha_egreso, telefono, email, mascota, primera_vez, observaciones))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('crear.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
