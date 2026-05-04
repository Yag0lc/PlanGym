from database.db import db


class Rutina(db.Model):
    __tablename__ = "rutinas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    activa = db.Column(db.Boolean, default=False, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    ejercicios = db.relationship("RutinaEjercicio", backref="rutina", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Rutina {self.nombre}>"