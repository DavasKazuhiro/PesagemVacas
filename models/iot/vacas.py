from models.db import db

class Vaca(db.Model):
    __tablename__ = 'vaca'
    id_vaca= db.Column('id_vaca', db.Integer, primary_key=True)
    rfid= db.Column(db.String(50))
    data_nascimento= db.Column(db.String(50))
    nome= db.Column(db.String(50))

    def get_vacas():
        return Vaca.query.all()
