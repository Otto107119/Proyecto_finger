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
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # ===== DATOS GENERALES =====
    fecha_formulario = db.Column(db.Date)
    fecha_nacimiento = db.Column(db.Date)
    estado_civil = db.Column(db.String(30))
    numero_contacto = db.Column(db.String(20))
    domicilio = db.Column(db.String(250))
    grado_escolaridad = db.Column(db.String(50))
    familiar_confianza_nombre = db.Column(db.String(120))
    familiar_confianza_telefono = db.Column(db.String(20))
    expectativas_participacion = db.Column(db.Text)

    # ===== ANTECEDENTES PERSONALES PATOLÓGICOS =====
    padece_enfermedad_actual = db.Column(db.Boolean, default=False)
    enfermedad_actual_detalle = db.Column(db.Text)

    consume_medicamentos = db.Column(db.Boolean, default=False)
    medicamentos_detalle = db.Column(db.Text)

    cirugias_previas = db.Column(db.Boolean, default=False)
    cirugias_detalle = db.Column(db.Text)

    problemas_vision = db.Column(db.Boolean, default=False)
    problemas_audicion = db.Column(db.Boolean, default=False)

    impedimento_actividad_fisica = db.Column(db.Boolean, default=False)
    impedimento_detalle = db.Column(db.Text)

    usa_dispositivo_apoyo = db.Column(db.Boolean, default=False)
    dispositivo_apoyo_detalle = db.Column(db.Text)

    # ===== SOCIODEMOGRÁFICO =====
    situacion_laboral_actual = db.Column(db.String(50))
    ocupacion_profesion_anterior = db.Column(db.String(120))
    fuente_principal_ingresos = db.Column(db.String(80))
    situacion_economica_actual = db.Column(db.String(50))

    cuenta_seguro_salud = db.Column(db.Boolean, default=False)
    recibe_ayuda_economica = db.Column(db.Boolean, default=False)

    tipo_vivienda = db.Column(db.String(50))
    condicion_vivienda = db.Column(db.String(50))
    personas_hogar = db.Column(db.Integer)
    rol_hogar = db.Column(db.String(80))

    participa_actividades_sociales = db.Column(db.Boolean, default=False)
    frecuencia_actividad_fisica = db.Column(db.String(50))
    situacion_sociodemografica_adicional = db.Column(db.Text)

    # ===== OBSERVACIONES =====
    observaciones_entrevista = db.Column(db.Text)

    # ===== RELACIONES =====
    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="historiales_clinicos")
    usuario = db.relationship("Usuario")