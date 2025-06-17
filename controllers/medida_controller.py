from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.medida_animal import MedidaAnimal
from datetime import datetime

medida_ = Blueprint("medida_", __name__, template_folder="views")

@medida_.route('/api/medidas', methods=['GET'])
def get_medidas():
    medidas = MedidaAnimal.query.all()
    medidas_data = [
        {
            'id_medida': m.id_medida,
            'id_vaca': m.id_vaca,
            'data_hora': m.data_hora.strftime('%Y-%m-%d %H:%M:%S') if m.data_hora else None,
            'altura_cm': m.altura_cm,
            'circ_peito_cm': m.circ_peito_cm
        }
        for m in medidas
    ]
    return jsonify(medidas_data)

@medida_.route('/api/edit_medida', methods=['POST'])
def edit_medida():
    data = request.get_json()

    id_medida = data.get('id') or data.get('id_medida')

    if not id_medida:
        return jsonify({'error': 'ID da medida é obrigatório'}), 400

    medida = MedidaAnimal.query.filter_by(id_medida=id_medida).first()
    if not medida:
        return jsonify({'error': 'Medida não encontrada'}), 404

    medida.id_vaca = data.get('id_vaca', medida.id_vaca)

    data_hora_str = data.get('data_hora')
    if data_hora_str:
        try:
            medida.data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Formato de data_hora inválido. Use YYYY-MM-DD HH:MM:SS'}), 400

    medida.altura_cm = data.get('altura_cm', medida.altura_cm)
    medida.circ_peito_cm = data.get('circ_peito_cm', medida.circ_peito_cm)

    from models.db import db
    db.session.commit()

    return jsonify({'message': f'Medida {id_medida} atualizada com sucesso'}), 200

