from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

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
    nombre = db.Column(db.String(120), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="pacientes")


class ActividadFisica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    duracion_min = db.Column(db.Integer, nullable=False)  # minutos
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_fisicas")
    usuario = db.relationship("Usuario")

class ActividadCognitiva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actividad = db.Column(db.String(150), nullable=False)
    resultado = db.Column(db.String(300))
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_cognitivas")
    usuario = db.relationship("Usuario")


class ActividadNutricional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_comida = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    calorias = db.Column(db.Integer)
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_nutricionales")
    usuario = db.relationship("Usuario")


class ActividadMedica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    presion_arterial = db.Column(db.String(20))
    glucosa = db.Column(db.String(20))
    peso = db.Column(db.Float)
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_medicas")
    usuario = db.relationship("Usuario")


class ActividadSocial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actividad = db.Column(db.String(150), nullable=False)
    duracion_min = db.Column(db.Integer)
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_sociales")
    usuario = db.relationship("Usuario")


class HistorialClinico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    motivo_consulta = db.Column(db.String(300))
    antecedentes_personales = db.Column(db.Text)
    antecedentes_familiares = db.Column(db.Text)
    padecimientos_actuales = db.Column(db.Text)
    medicamentos = db.Column(db.Text)
    alergias = db.Column(db.Text)
    observaciones = db.Column(db.Text)

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="historiales_clinicos")
    usuario = db.relationship("Usuario")