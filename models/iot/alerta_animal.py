from models.db import db
from datetime import datetime


class Alerta(db.Model):
    __tablename__ = 'alerta'
    id_alerta= db.Column('id_vaca', db.Integer, primary_key=True)
    id_vaca = db.Column(db.Integer,db.ForeignKey('vaca.id_vaca'), nullable=False)
    data_hora  = db.Column(db.DateTime, default=datetime.utcnow) 
    tipo_alerta = db.Column(db.String(50))

    @staticmethod
    def get_alertas():
        return Alerta.query.all()
