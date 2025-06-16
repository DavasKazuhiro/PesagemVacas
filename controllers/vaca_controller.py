from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.vacas import Vaca
from models.db import db

vaca_ = Blueprint("vaca_", __name__, template_folder="views")

@vaca_.route('/api/vacas', methods=['GET'])
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

@vaca_.route('/api/add_vaca', methods=['POST'])
def add_vaca():
    data = request.get_json()
    rfid = data.get('rfid')
    data_nascimento = data.get('data_nascimento')
    nome = data.get('nome')
    if not (rfid and data_nascimento and nome):
        return jsonify({'error': 'RFID, data de nascimento e nome são obrigatórios.'}), 400
    vaca = Vaca(nome=nome, data_nascimento=data_nascimento, rfid=rfid)
    db.session.add(vaca)
    db.session.commit()
    return jsonify({'message': 'Vaca adicionada com sucesso.'}), 201

@vaca_.route('/api/delete_vaca', methods=['POST'])
def delete_vaca():
    data = request.get_json()
    id_vaca = data.get('id_vaca')

    if not id_vaca:
        return jsonify({'error': 'ID é obrigatório'}), 400

    vaca = Vaca.query.filter_by(id_vaca=id_vaca).first()
    if vaca:
        from models.db import db
        db.session.delete(vaca)
        db.session.commit()
        return jsonify({'message': f'Vaca "{vaca.nome}" removida com sucesso'}), 200
    else:
        return jsonify({'error': 'Vaca não encontrada'}), 404