from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80), nullable = False)
	clave = db.Column(db.String(120), nullable = False)    
	tipo = db.Column(db.String(80), nullable = False)
	dni = db.Column(db.Integer, unique = True, nullable = False)
	#viaje = db.relationship('Viaje', backref='usuario', cascade="all, delete-orphan" , lazy='dynamic')

	def __init__(self, nombre, clave, dni):
		self.nombre = nombre
		self.clave = clave
		self.dni = dni
		self.tipo = 'Usuario'

	def acender(self):
		self.tipo = 'Operador'

class Viajeee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	origen = db.Column(db.String(80), nullable=False)
	destino = db.Column(db.String(80), nullable=False)
	fecha = db.Column(db.String(80), nullable=False)
	demora = db.Column(db.Integer, nullable=False)
	duracion = db.Column(db.Integer, nullable=False)
	importe = db.Column(db.String(80), nullable=False)
	dniCliente = db.Column(db.String(80), nullable=False)
	numMovil = db.Column(db.String(80), nullable=False)
	
	def __init__(self, o, des,dnic,dem,dur,imp,numMovil):
		self.origen = o
		self.destino = des
		self.fecha = str(date.today())
		self.demora = dem
		self.duracion = dur
		self.importe = imp
		self.dniCliente = dnic
		self.numMovil = numMovil
class Movil(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	numero = db.Column(db.Integer, unique = True, nullable = False)
	patente = db.Column(db.String(80), nullable = False)
	marca = db.Column(db.String(80), nullable = False)
	#viaje = db.relationship('Viaje', backref='user', cascade="all, delete-orphan" , lazy='dynamic')

	def __init__(self, numero, patente, marca):
		self.numero = numero
		self.patente = patente
		self.marca = marca