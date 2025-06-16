from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.usuario import Usuario
from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash

user_ = Blueprint("user_", __name__, template_folder="views")

@user_.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    from models.iot.usuario import Usuario
    usuarios = Usuario.query.all()
    usuarios_data = [
        {
            'id_usuario': u.id_usuario,
            'nivel_usuario': u.nivel_usuario,
            'nome': u.nome,
            'email': u.email,
            'criado_em': u.criado_em.strftime('%Y-%m-%d %H:%M:%S') if u.criado_em else None
        }
        for u in usuarios
    ]
    return jsonify(usuarios_data)

@user_.route('/api/add_user', methods=['POST'])
def add_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    nivel_usuario = data.get('nivel_usuario')
    senha = generate_password_hash(data.get('senha'))

    if not (nome and email and nivel_usuario and senha):
        return jsonify({'error': 'Nome, email, nível de usuário e senha são obrigatórios.'}), 400

    usuario = Usuario(nome=nome, email=email, nivel_usuario=nivel_usuario, senha=senha)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário adicionado com sucesso.'}), 201

@user_.route('/api/delete_user', methods=['POST'])
def delete_usuario():
    data = request.get_json()
    id_usuario = data.get('id_usuario')

    if not id_usuario:
        return jsonify({'error': 'ID is required'}), 400

    usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': f'Usuário "{usuario.nome}" deletado com sucesso'}), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404
