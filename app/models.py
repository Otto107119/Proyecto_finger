from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="capturista")

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    edad = db.Column(db.Integer)

    actividad_fisica = db.relationship('ActividadFisica', backref='paciente')
    actividad_cognitiva = db.relationship('ActividadCognitiva', backref='paciente')
    actividad_nutricional = db.relationship('ActividadNutricional', backref='paciente')
    actividad_medica = db.relationship('ActividadMedica', backref='paciente')
    actividad_social = db.relationship('ActividadSocial', backref='paciente')
    historial_clinico = db.relationship('HistorialClinico', backref='paciente')

class ActividadFisica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100))
    duracion = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class ActividadCognitiva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actividad = db.Column(db.String(100))
    resultado = db.Column(db.String(200))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class ActividadNutricional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comida = db.Column(db.String(200))
    calorias = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class ActividadMedica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    presion = db.Column(db.String(20))
    glucosa = db.Column(db.String(20))
    observaciones = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class ActividadSocial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actividad = db.Column(db.String(200))
    duracion = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class HistorialClinico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    medicamentos = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))


