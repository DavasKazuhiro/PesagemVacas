from models.db import db
from models.iot.vacas import Vaca

class Pesagem(db.Model):
    __tablename__ = 'pesagem'
    id_pesagem= db.Column('id_pesagem', db.Integer, primary_key=True)
    data_hora= db.Column(db.DateTime)
    valor= db.Column(db.Float)
    
    id_vaca = db.relationship('Vaca', backref='pesagem', lazy=True)

    def save_pesagem(data_hora, valor, id_vaca):
        pesagem = Pesagem(data_hora = data_hora, valor = valor, id_vaca = id_vaca)

        db.session.add(pesagem)
        db.session.commit()

    def get_pesagem():
        pesagens = Pesagem.query.join(Vaca, Vaca.id_vaca == Pesagem.vaca_id)\
            .add_columns(Vaca.id_vaca, Vaca.nome, Pesagem.data_hora, Pesagem.valor).all()
        
        return pesagens