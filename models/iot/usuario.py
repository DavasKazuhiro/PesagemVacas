from models.db import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario     = db.Column(db.Integer, primary_key=True)       
    nivel_usuario  = db.Column(db.String(50),  nullable=False)     
    nome           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(100), unique=True, nullable=False)
    criado_em      = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_usuarios():
        return Usuario.query.all()
    