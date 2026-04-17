from datetime import datetime, date
from app import db


class Paciente(db.Model):
    __tablename__ = "paciente"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="pacientes")

    actividad_social = db.relationship(
        "ActividadSocial",
        back_populates="paciente",
        uselist=False,
        cascade="all, delete-orphan"
    )

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return ""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad