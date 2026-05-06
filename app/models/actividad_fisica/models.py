from datetime import datetime
from app import db


class ActividadFisica(db.Model):
    __tablename__ = "actividad_fisica"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("paciente.id"),
        nullable=False
    )

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Pruebas físicas generales
    sentarse_levantarse_30s = db.Column(db.Integer)
    dinamometro_kg = db.Column(db.Float)
    tug_segundos = db.Column(db.Float)
    equilibrio_unipodal_segundos = db.Column(db.Float)
    caminata_6min_metros = db.Column(db.Float)
    velocidad_marcha_ms = db.Column(db.Float)

    # SPPB
    sppb_equilibrio = db.Column(db.Integer)
    sppb_velocidad_marcha = db.Column(db.Integer)
    sppb_fuerza_piernas = db.Column(db.Integer)
    sppb_total = db.Column(db.Integer)

    interpretacion_sppb = db.Column(db.String(100))
    riesgo_caida = db.Column(db.String(100))
    riesgo_funcional = db.Column(db.String(100))

    notas = db.Column(db.Text)

    def calcular_resultados(self):
        total = (
            (self.sppb_equilibrio or 0)
            + (self.sppb_velocidad_marcha or 0)
            + (self.sppb_fuerza_piernas or 0)
        )

        self.sppb_total = total

        if total <= 3:
            self.interpretacion_sppb = "Muy bajo"
        elif total <= 6:
            self.interpretacion_sppb = "Bajo"
        elif total <= 9:
            self.interpretacion_sppb = "Moderado"
        else:
            self.interpretacion_sppb = "Buen rendimiento"

        if self.tug_segundos is not None:
            if self.tug_segundos > 10:
                self.riesgo_caida = "Riesgo de caída / movilidad reducida"
            else:
                self.riesgo_caida = "Movilidad conservada"

        if self.velocidad_marcha_ms is not None:
            if self.velocidad_marcha_ms < 0.8:
                self.riesgo_funcional = "Riesgo funcional"
            elif self.velocidad_marcha_ms >= 1.0:
                self.riesgo_funcional = "Buena capacidad funcional"
            else:
                self.riesgo_funcional = "Capacidad funcional intermedia"