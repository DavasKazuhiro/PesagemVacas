from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.vacas import Vaca

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

@vaca_.route('/api/vacas/delete', methods=['POST'])
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