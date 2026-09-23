from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.secret_key = 'clave_secreta_examen'

usuarios = {
    "carlos": "1111",
    "laura": "2222",
    "diego": "3333"
}

lista_libros = [
    {"titulo": "Python desde cero", "autor": "Juan Pérez", "disponibles": 4},
    {"titulo": "Desarrollo Web", "autor": "María López", "disponibles": 2},
    {"titulo": "Inteligencia Artificial", "autor": "Pedro García", "disponibles": 0}
]



@app.route('/')
def index():
    ultimo_usuario = request.cookies.get('ultimo_usuario')
    return render_template('index.html', ultimo_usuario=ultimo_usuario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        password = request.form.get('contrasena')
        
        if user in usuarios and usuarios[user] == password:
            session['usuario'] = user  
            flash(f'¡Bienvenido, {user}!', 'success')  
            
            resp = make_response(redirect(url_for('libros')))
            resp.set_cookie('ultimo_usuario', user)
            return resp
        else:
            flash('Usuario o contraseña incorrectos.', 'danger') 

    return render_template('login.html')

@app.route('/libros')
def libros():
    return render_template('libros.html', libros=lista_libros)

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

#eliminar la cookie
@app.route('/eliminar_cookie')
def eliminar_cookie():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('ultimo_usuario', '', expires=0) # Borra la cookie expirándola al instante
    flash('La cookie de último usuario ha sido eliminada.', 'info')
    return resp

if __name__ == '__main__':
    app.run(debug=True)