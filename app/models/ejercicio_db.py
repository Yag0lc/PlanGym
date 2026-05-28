from database.db import db


class RutinaEjercicio(db.Model):
    __tablename__ = "rutina_ejercicios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False, default="lunes")
    id_rutina = db.Column(db.Integer, db.ForeignKey("rutinas.id"), nullable=False)

    def __repr__(self):
        return f"<Ejercicio {self.nombre} - {self.dia_semana}>"
