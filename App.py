from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'WebJhon'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contactos = data)

@app.route('/add_contactos', methods=['POST'])
def add_contactos():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Telefono = request.form['Telefono']
        Correo = request.form['Correo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contactos (Nombre, Telefono, Correo) VALUES (%s,%s,%s)", (Nombre, Telefono, Correo))
        mysql.connection.commit()
        flash('contacto Agregado Con Exito')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contactos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contactos.html', contactos = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Telefono = request.form['Telefono']
        Correo = request.form['Correo']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Contactos
            SET Nombre = %s,
                Correo = %s,
                Telefono = %s
            WHERE id = %s
        """, (Nombre, Correo, Telefono, id))
        flash('Contacto Actualizado Con Exito')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado Con Exito')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)