from models.db import db
from models.iot.vacas import Vaca
from datetime import datetime


class Alerta(db.Model):
    __tablename__ = 'alerta'
    id_alerta= db.Column(db.Integer, primary_key=True)
    id_vaca = db.Column(db.Integer,db.ForeignKey('vaca.id_vaca'), nullable=False)
    data_hora  = db.Column(db.DateTime, default=datetime.utcnow) 
    tipo_alerta = db.Column(db.String(50))

    vaca = db.relationship('Vaca', backref='alerta', lazy=True)

    @staticmethod
    def save_alerta(id_vaca: int, tipo_alerta: str, data_hora: datetime = None):
        alerta = Alerta(
            id_vaca  = id_vaca,
            tipo_alerta= tipo_alerta,
            data_hora= data_hora or datetime.utcnow()
        )
        db.session.add(alerta)
        db.session.commit()
        return alerta

    @staticmethod
    def get_alertas():
        return Alerta.query.all()
