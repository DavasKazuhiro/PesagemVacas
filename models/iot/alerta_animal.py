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
    def get_alertas():
        return Alerta.query.all()
