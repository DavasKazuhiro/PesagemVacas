from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.iot.pesagens import Pesagem

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




