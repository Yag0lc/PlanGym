from database.db import db


class DiaCompletado(db.Model):
    __tablename__ = "dias_completados"

    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def __repr__(self):
        return f"<DiaCompletado {self.dia}/{self.mes}/{self.anio}>"