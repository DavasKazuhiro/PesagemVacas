from models.db import db
from models.iot.vacas import Vaca
from datetime import datetime

class MedidaAnimal(db.Model):
    __tablename__ = 'medida_animal'
    id_medida       = db.Column(db.Integer, primary_key=True)
    id_vaca         = db.Column(db.Integer,db.ForeignKey('vaca.id_vaca'),nullable=False)
    data_hora       = db.Column(db.DateTime, default=datetime.utcnow) 
    altura_cm       = db.Column(db.Float, nullable=True)
    circ_peito_cm   = db.Column(db.Float, nullable=True)
    vaca = db.relationship(
        'Vaca',
        backref=db.backref('medidas', lazy=True)
    )

    @staticmethod
    def save_medida(id_vaca, altura_cm, circ_peito_cm, data_hora=None):
        medida = MedidaAnimal(
            id_vaca       = id_vaca,
            data_hora     = data_hora or datetime.utcnow(),
            altura_cm     = altura_cm,
            circ_peito_cm = circ_peito_cm
        )
        db.session.add(medida)
        db.session.commit()
        return medida

    @staticmethod
    def get_medidas():
        return (MedidaAnimal.query
                .join(Vaca, Vaca.id_vaca == MedidaAnimal.id_vaca)
                .add_columns(
                    MedidaAnimal.id_medida,
                    MedidaAnimal.data_hora,
                    MedidaAnimal.altura_cm,
                    MedidaAnimal.circ_peito_cm,
                    Vaca.id_vaca,
                    Vaca.nome
                ).all())
