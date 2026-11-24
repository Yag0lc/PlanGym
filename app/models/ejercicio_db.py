from database.db import db


class RutinaEjercicio(db.Model):
    __tablename__ = "rutina_ejercicios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False, default="lunes")
    id_rutina = db.Column(db.Integer, db.ForeignKey("rutinas.id"), nullable=False)

    def __repr__(self):
        return f"<Ejercicio {self.nombre} - {self.dia_semana}>"


class RegistroEjercicio(db.Model):
    __tablename__ = "registros_ejercicios"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False, default=0)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_rutina_ejercicio = db.Column(
        db.Integer, db.ForeignKey("rutina_ejercicios.id"), nullable=False
    )

    ejercicio = db.relationship("RutinaEjercicio", backref="registros")
