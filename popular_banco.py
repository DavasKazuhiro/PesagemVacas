from controllers.app_controller import create_app
from models.db import db
from models.iot.vacas import Vaca
from models.iot.pesagens import Pesagem
from datetime import datetime, date

def popular_banco():
    app = create_app()
    
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Dados das vacas do SQL
        vacas_dados = [
            (1, '[254, 47, 127, 94, 240]', '2021-03-14', 'Mimosa'),
            (2, '[134, 72, 25, 126, 169]', '2020-07-22', 'Luzia'),
            (3, '[140, 55, 18, 145, 230]', '2019-11-30', 'Estrela'),
            (4, '[138, 70, 20, 110, 210]', '2021-01-10', 'Aurora'),
            (5, '[133, 74, 29, 120, 250]', '2022-05-25', 'Branquinha'),
            (6, '[137, 68, 26, 105, 198]', '2020-09-09', 'Pretinha'),
            (7, '[142, 69, 27, 130, 215]', '2021-12-18', 'Pintada'),
            (8, '[135, 71, 22, 112, 199]', '2018-06-03', 'Serena'),
            (9, '[139, 64, 24, 118, 205]', '2019-10-16', 'Nuvem'),
            (10, '[136, 73, 28, 108, 202]', '2020-02-27', 'Tempestade')
        ]
        
        # Inserir vacas
        for id_vaca, rfid, data_nasc, nome in vacas_dados:
            vaca_existente = Vaca.query.filter_by(id_vaca=id_vaca).first()
            if not vaca_existente:
                vaca = Vaca(
                    id_vaca=id_vaca,
                    rfid=rfid,
                    data_nascimento=datetime.strptime(data_nasc, '%Y-%m-%d').date(),
                    nome=nome
                )
                db.session.add(vaca)
        
        # Dados das pesagens do SQL
        pesagens_dados = [
            (1, '2025-06-14 01:40:04', 640.65, 2),
            (2, '2025-06-14 01:42:11', 542.22, 2),
            (3, '2025-06-14 01:45:36', 621.13, 2)
        ]
        
        # Inserir pesagens
        for id_pesagem, data_hora, valor, id_vaca in pesagens_dados:
            pesagem_existente = Pesagem.query.filter_by(id_pesagem=id_pesagem).first()
            if not pesagem_existente:
                pesagem = Pesagem(
                    id_pesagem=id_pesagem,
                    data_hora=data_hora,
                    valor=valor,
                    id_vaca=id_vaca
                )
                db.session.add(pesagem)
        
        db.session.commit()
        print("Banco populado com sucesso!")
        
        # Verificar dados inseridos
        vacas = Vaca.query.all()
        pesagens = Pesagem.query.all()
        print(f"Vacas inseridas: {len(vacas)}")
        print(f"Pesagens inseridas: {len(pesagens)}")

if __name__ == "__main__":
    popular_banco() 