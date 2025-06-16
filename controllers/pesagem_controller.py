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
            'tipo_alerta': a.tipo_alerta
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

@pesagem_.route('/api/alertas', methods=['POST'])
def create_alerta():
    data = request.get_json()
    id_vaca   = data.get('id_vaca')
    tipo_alerta = data.get('tipo_alerta')

    if not (id_vaca and tipo_alerta):
        return jsonify({'error': 'Campos id_vaca e tipo_alerta são obrigatórios.'}), 400

    alerta = Alerta.save_alerta(id_vaca=id_vaca, tipo_alerta=tipo_alerta)
    return jsonify({
        'id_alerta': alerta.id_alerta,
        'id_vaca'  : alerta.id_vaca,
        'data_hora': alerta.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
        'tipo_alerta': alerta.tipo_alerta
    }), 201



@pesagem_.route('/api/vacas/delete', methods=['POST'])
def delete_vaca():
    data = request.get_json()
    nome = data.get('nome')

    if not nome:
        return jsonify({'error': 'Name is required'}), 400

    vaca = Vaca.query.filter_by(nome=nome).first()
    if vaca:
        from models.db import db
        db.session.delete(vaca)
        db.session.commit()
        return jsonify({'message': f'Vaca "{nome}" deleted successfully'}), 200
    else:
        return jsonify({'error': 'Cow not found'}), 404

@pesagem_.route('/api/remove_user', methods=['POST'])
def remove_user():
    from models.db import db  # make sure db is imported
    from models.iot.usuario import Usuario


    data = request.get_json()
    user_id = data.get('id_usuario')  # match frontend key

    if not user_id:
        return jsonify({'error': 'Missing user ID'}), 400

    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User removed successfully'}), 200

@pesagem_.route('/api/add_user', methods=['POST'])
def add_user():
    from models.db import db
    from models.iot.usuario import Usuario

    data = request.get_json()

    nome = data.get('nome')
    email = data.get('email')
    nivel_usuario = data.get('nivel_usuario')

    if not all([nome, email, nivel_usuario]):
        return jsonify({'error': 'Missing fields'}), 400

    existing_user = Usuario.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409

    novo_usuario = Usuario(nome=nome, email=email, nivel_usuario=nivel_usuario)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'User added successfully', 'id_usuario': novo_usuario.id_usuario}), 201

