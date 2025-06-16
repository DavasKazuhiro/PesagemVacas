from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.alerta_animal import Alerta

alerta_ = Blueprint("alerta_", __name__, template_folder="views")

@alerta_.route('/api/alertas', methods=['GET'])
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

@alerta_.route('/api/alertas', methods=['POST'])
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