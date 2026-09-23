from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta_examen'

usuarios = {
    "carlos": "1111",
    "laura": "2222",
    "diego": "3333"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        password = request.form.get('contrasena')
        # Verificar si el usuario existe y la contraseña coincide
        if user in usuarios and usuarios[user] == password:
            session['usuario'] = user  
            flash(f'¡Bienvenido, {user}!', 'success')  
            return redirect(url_for('libros'))  
        else:
            flash('Usuario o contraseña incorrectos.', 'danger') 

    return render_template('login.html')

@app.route('/libros')
def libros():
    return render_template('libros.html')

@app.route('/perfil')
def perfil():
    # Ruta protegida
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    return render_template('perfil.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)