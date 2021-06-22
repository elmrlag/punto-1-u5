from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')
DNI = -1
from models import db
from models import User
from models import Viajeee
#from models import Movil
@app.route('/')
def inicio():
	return render_template('inicio.html')

@app.route('/registrarse', methods = ['GET','POST'])
def registrarse():
    if request.method == 'POST':
        if not request.form['dni'] or not request.form['nombre'] or not request.form['clave']:
            return render_template('error.html', error="Por favor, complete todos los campos")
        else:
            usuario = User(
                nombre = request.form['nombre'],
                clave = generate_password_hash(request.form['clave']),
                dni = request.form['dni']
            )
            db.session.add(usuario)
            db.session.commit()
            return render_template('aviso.html', mensaje="El usuario se registró exitosamente")
    return render_template('nuevo_usuario.html')

@app.route('/ingresar', methods = ['GET','POST'])
def ingresar():
    if request.method == 'POST':
        if  not request.form['dni'] or not request.form['clave']:
            return render_template('error.html', error="Rellene todos los campos")
        else:
            usuario_actual= User.query.filter_by(dni = request.form['dni']).first()
            if usuario_actual is None:
                return render_template('error.html', error="El documento no está registrado")
            else:
                verificacion = check_password_hash(usuario_actual.clave, request.form['clave'])
                if (verificacion):
                    return redirect(url_for('UsuarioNormal', nombre= usuario_actual.nombre))
                else:
                    return render_template('error.html', error="Clave errónea")
    else:
        return render_template('ingresar.html')

@app.route('/Usuario/<nombre>')
def UsuarioNormal(nombre):
    return render_template('Usuario.html', Nombre=nombre)

@app.route('/Operador')
def operador(UsuarioActual):
    return render_template('Operador.html')

@app.route('/PedirMovil', methods = ['GET','POST'])
def PedirMovil():
    if request.method == 'POST':
        if (not request.form['DireccionO'] or not request.form['DireccionD']):
            return render_template('error.html', error="Rellene todos los campos")
        else:
            viaje = Viajeee(request.form['DireccionO'], request.form['DireccionD'], request.form['DNI'], 0, 0, 0, 0)
            db.session.add(viaje)
            db.session.commit()
            return render_template('aviso.html', mensaje="El movil se pidio correctamente")
    else:
        return render_template('PedirMovil.html')

@app.route('/AsignarUnMovil', methods = ['GET','POST'])
def AsignarUnMovil():
    if request.method == 'POST':
        if  not request.form['Pedidos'] or not request.form['NMovil'] or not request.form['Demora']:
            return render_template('error.html', error="Rellene todos los campos")
        else:
            Aux=Viajeee.query.all()
            for viaje in Aux:
                if viaje.id==request.form['Pedidos']:
                    viajeAux = Viajeee(
                        viaje.origen, 
                        viaje.destino, 
                        viaje.dniCliente, 
                        request.form['Demora'], 
                        0, 
                        0, 
                        request.form['NMovil'])
                    db.session.delete(viaje)
                    db.session.add(viajeAux)
                    db.session.commit()
            return render_template('aviso.html', mensaje="El viaje se asigno correctamente")
    else:
        return render_template('AsignarUnMovil.html',viajes=Viajeee.query.all())

@app.route('/VolverseOperador', methods = ['GET','POST'])
def VolverseOperador():
    if request.method == 'POST':
        if (request.form['password']=="Admin"):
            return render_template('Operador.html')
        else:
            return render_template('error.html', error="La contraseña no es válida")
    else:
        return render_template('VolverseOperador.html')

@app.route('/bienvenida/<leng>')
def bienvenida(leng):
    if leng == 'es':
        return render_template('bienvenida.html', saludo='Hola!')
    else:
        return render_template('bienvenida.html', saludo='Hello')

@app.route('/listar_viajes')
def listar_viajes():
    return render_template('listar_viajes.html', viajes=Viajeee.query.all())

@app.route('/consultar_estado_movil', methods = ['GET','POST'])
def consultar_estado_movil():
    listaAux = []
    if request.method == 'POST':
        if  not request.form['dni']:
            return render_template('error.html', error="Rellene todos los campos")
        else:
            usuario_actual= User.query.filter_by(dni = request.form['dni']).first()
            if usuario_actual is None:
                return render_template('error.html', error="El documento no está registrado")
            else:
                viajes = Viajeee.query.all()
                for viaje in viajes:
                    if viaje.dniCliente == request.form['dni']:
                        listaAux.append(viaje)
    else:
        return render_template('consultar_estado_movil.html')
    if len(listaAux) <= 0:
        return render_template('aviso.html', mensaje="“No existen solicitudes pendientes")
    else:
        return render_template('estado_movil.html', lista = listaAux)

@app.route('/Finalizar', methods = ['GET','POST'])
def Finalizar():
    if request.method == 'POST':
        if not request.form['Pedidos'] or not request.form['Duracion']:
            return render_template('error.html', error="Rellene todos los campos")
        else:
            Aux = Viajeee.query.all()
            for viaje in Aux:
                if int(viaje.id) == int(request.form['Pedidos']):
                    importe = 100+ 5 * int(request.form['Duracion'])
                    if(viaje.demora>15):
                        importe=importe-((10 * importe)/100)
                    viajeAux = Viajeee(
                        viaje.origen,
                        viaje.destino,
                        viaje.dniCliente,
                        viaje.demora,
                        request.form['Duracion'],
                        importe,
                        viaje.numMovil
                    )
                    db.session.delete(viaje)
                    db.session.add(viajeAux)
                    db.session.commit()
            return render_template('aviso.html', mensaje="Se finalizo el viaje")
    else:
        return render_template('Finalizar.html', viajes=Viajeee.query.all())

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)