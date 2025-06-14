#sensors_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.pesagens import Pesagem
from models.iot.vacas import Vaca
from models.iot.medida_animal import MedidaAnimal
from models.iot.alerta_animal import Alerta
from models.iot.usuario import Usuario



pesagem_ = Blueprint("pesagem_", __name__ , template_folder="views")

@pesagem_.route('/api/pesagens', methods=['GET'])
def get_pesagens():
    pesagens = Pesagem.query.all()
    result = [{
        "id_vaca": p.id_vaca,
        "pesagem": p.valor,
        "data_hora": p.data_hora
    } for p in pesagens]
    return jsonify(result)

@pesagem_.route('/api/vacas', methods=['GET'])
def get_vacas():
    vacas = Vaca.query.all()
    vacas_data = [
        {
            'id_vaca': v.id_vaca,
            'rfid': v.rfid,
            'data_nascimento': v.data_nascimento.strftime('%Y-%m-%d') if v.data_nascimento else None,
            'nome': v.nome
        }
        for v in vacas
    ]
    return jsonify(vacas_data)

@pesagem_.route('/api/medidas', methods=['GET'])
def get_medidas():
    from models.iot.medida_animal import MedidaAnimal
    medidas = MedidaAnimal.query.all()
    medidas_data = [
        {
            'id_medida': m.id_medida,
            'id_vaca': m.id_vaca,
            'data_hora': m.data_hora.strftime('%Y-%m-%d %H:%M:%S') if m.data_hora else None,
            'tipo': m.tipo,
            'valor': m.valor
        }
        for m in medidas
    ]
    return jsonify(medidas_data)

@pesagem_.route('/api/alertas', methods=['GET'])
def get_alertas():
    from models.iot.alerta_animal import Alerta
    alertas = Alerta.query.all()
    alertas_data = [
        {
            'id_alerta': a.id_alerta,
            'id_vaca': a.id_vaca,
            'data_hora': a.data_hora.strftime('%Y-%m-%d %H:%M:%S') if a.data_hora else None,
            'descricao': a.descricao
        }
        for a in alertas
    ]
    return jsonify(alertas_data)

@pesagem_.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    from models.iot.usuario import Usuario
    usuarios = Usuario.query.all()
    usuarios_data = [
        {
            'id_usuario': u.id_usuario,
            'nivel_usuario': u.nivel_usuario,
            'nome': u.nome,
            'data_criacao': u.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if u.data_criacao else None
        }
        for u in usuarios
    ]
    return jsonify(usuarios_data)




