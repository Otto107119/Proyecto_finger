from datetime import datetime
from app import db


class ActividadSocial(db.Model):
    __tablename__ = "actividad_social"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("paciente.id", ondelete="CASCADE"),
        nullable=False
    )

    seguridad_social = db.Column(db.String(20), nullable=True)
    tiempo_residencia_ameca = db.Column(db.Integer, nullable=True)
    tipo_vivienda = db.Column(db.String(20), nullable=True)
    migracion = db.Column(db.Boolean, default=False, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    
    finalizado = db.Column(db.Boolean, default=False, nullable=False)
    fecha_finalizado = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    paciente = db.relationship("Paciente", back_populates="actividades_sociales")

    economia = db.relationship(
        "ActividadSocialEconomia",
        back_populates="actividad_social",
        uselist=False,
        cascade="all, delete-orphan"
    )

    salud_mental = db.relationship(
        "ActividadSocialSaludMental",
        back_populates="actividad_social",
        uselist=False,
        cascade="all, delete-orphan"
    )

    gds15 = db.relationship(
        "ActividadSocialGDS15",
        back_populates="actividad_social",
        uselist=False,
        cascade="all, delete-orphan"
    )

    katz = db.relationship(
        "ActividadSocialKatz",
        back_populates="actividad_social",
        uselist=False,
        cascade="all, delete-orphan"
    )

    lawton_brody = db.relationship(
        "ActividadSocialLawtonBrody",
        back_populates="actividad_social",
        uselist=False,
        cascade="all, delete-orphan"
    )

    padres = db.relationship(
        "ActividadSocialPadreMadre",
        back_populates="actividad_social",
        cascade="all, delete-orphan"
    )

    hermanos = db.relationship(
        "ActividadSocialHermano",
        back_populates="actividad_social",
        cascade="all, delete-orphan"
    )

    hijos = db.relationship(
        "ActividadSocialHijo",
        back_populates="actividad_social",
        cascade="all, delete-orphan"
    )
    

    def __repr__(self):
        return f"<ActividadSocial paciente_id={self.paciente_id}>"