from models.db import db
from models.iot.vacas import Vaca

class Pesagem(db.Model):
    __tablename__ = 'pesagem'
    
    id_pesagem = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.String(50))
    valor = db.Column(db.Float)
    
    # Coluna que referencia a vaca
    id_vaca = db.Column(db.Integer, db.ForeignKey('vaca.id_vaca'), nullable=False)

    # Relacionamento com a tabela Vaca
    vaca = db.relationship('Vaca', backref='pesagens', lazy=True)

    @staticmethod
    def save_pesagem(data_hora, valor, rfid):
        vaca = Vaca.query.filter_by(rfid=rfid).first()

        if vaca is None:
            print(f"Vaca com RFID {rfid} não encontrada.")
            return

        pesagem = Pesagem(data_hora=data_hora, valor=valor, id_vaca=vaca.id_vaca)
        db.session.add(pesagem)
        db.session.commit()
        print(f"Pesagem registrada para vaca ID {vaca.id_vaca}")

    @staticmethod
    def get_pesagem():
        pesagens = Pesagem.query.join(Vaca, Vaca.id_vaca == Pesagem.id_vaca)\
            .add_columns(Vaca.id_vaca, Vaca.nome, Pesagem.data_hora, Pesagem.valor).all()
        print("enviado")
        return pesagens
