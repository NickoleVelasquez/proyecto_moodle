from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib
from email.mime.text import MIMEText
import openpyxl
from openpyxl import Workbook
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Crear la base de datos con usuarios y roles si no existe
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insertar usuarios de ejemplo
def insert_example_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Comprobar si ya existen usuarios
    c.execute("SELECT * FROM users")
    if c.fetchone() is None:  # Si no hay usuarios, los insertamos
        c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
        c.execute("INSERT INTO users (username, password, role) VALUES ('user', 'user123', 'usuario')")
        conn.commit()
    conn.close()

# Verificar usuario en la base de datos
def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]  # Retorna el rol
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = check_user(username, password)

        if role:
            session['username'] = username
            session['role'] = role

            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'usuario':
                return redirect(url_for('user_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' in session:
        print(f"Role in session: {session['role']}")  # Verifica el valor del rol en la sesión
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', username=session['username'])
    else:
        flash('Acceso denegado. Inicie sesión como administrador.')
        return redirect(url_for('login'))

@app.route('/garantias')
def garantias():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('garantias.html')

@app.route('/modulo1')
def modulo1():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('modulo1.html')

@app.route('/modulo2')
def modulo2():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('modulo2.html')

@app.route('/modulo3')
def modulo3():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('modulo3.html')

@app.route('/modulo4')
def modulo4():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('modulo4.html')

@app.route('/foros')
def foros():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('foros.html')

@app.route('/rehab')
def rehab():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('rehab.html')

@app.route('/rehab2')
def rehab2():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('rehab2.html')

@app.route('/psico')
def psico():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('psico.html')

@app.route('/psico2')
def psico2():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('psico2.html')

@app.route('/foros2')
def foros2():
    # Aquí deberías retornar la vista de la página de garantías
    return render_template('foros2.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'role' in session:
        print(f"Role in session: {session['role']}")  # Verifica el valor del rol en la sesión
    if 'role' in session and session['role'] == 'usuario':
        return render_template('user_dashboard.html', username=session['username'])
    else:
        flash('Acceso denegado. Inicie sesión como administrador.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        dob = request.form.get('dob')
        tutor = request.form.get('tutor', 'N/A')
        email = request.form.get('email')
        is_ab = request.form.get('is_ab')
        modelo = request.form.get('modelo', 'N/A')
        privacy = request.form.get('privacy', False)

        # Aquí puedes agregar la lógica de enviar por correo
        send_email(nombre, dob, tutor, email, is_ab, modelo)

        # Generar Excel
        generate_excel(nombre, dob, tutor, email, is_ab, modelo)

        return "Formulario enviado exitosamente."

    return render_template('register.html')


def send_email(nombre, dob, tutor, email, is_ab, modelo):
    # Configura los detalles del correo
    sender_email = 'velasqueznckole@gmail.com'  # Reemplaza con tu correo
    receiver_email = 'nickolevelasquezacosta@gmail.com'  # Reemplaza con el correo del destinatario

    # Configura Mailtrap SMTP
    smtp_server = 'smtp.mailtrap.io'
    smtp_port = 587  # O usa 2525 si el puerto 587 no funciona
    smtp_user = '449ab498653acd'  # Reemplaza con tu usuario de Mailtrap
    smtp_password = '7c7051f54f8fd1'  # Reemplaza con tu contraseña de Mailtrap

    # Crea el mensaje
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Nuevo registro de paciente'
    
    body = f"""
    Nombre del Paciente: {nombre}
    Fecha de Nacimiento: {dob}
    Nombre del Tutor: {tutor}
    Correo Electrónico: {email}
    ¿Es paciente de AB?: {is_ab}
    Modelo de Procesador: {modelo}
    """
    message.attach(MIMEText(body, 'plain'))

    # Envía el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Usa TLS para la conexión segura
            server.login(smtp_user, smtp_password)
            server.send_message(message)
            print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def generate_excel(nombre, dob, tutor, email, is_ab, modelo):
    file_path = "registro_pacientes.xlsx"

    if not os.path.exists(file_path):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Nombre", "Fecha de Nacimiento", "Tutor", "Email", "Es paciente de AB", "Modelo"])
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    
    sheet.append([nombre, dob, tutor, email, is_ab, modelo])
    workbook.save(file_path)

if __name__ == '__main__':
    init_db()  # Asegúrate de que la tabla users exista
    insert_example_users()  # Inserta usuarios de ejemplo si no hay ninguno
    app.run(debug=True)
