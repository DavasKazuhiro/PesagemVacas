from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.medida_animal import MedidaAnimal

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