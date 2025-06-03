#sensors_controller.py
from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.pesagens import Pesagem

pesagem_ = Blueprint("pesagem_", __name__ , template_folder="views")

@pesagem_.route('/pesagens')
def pesagens():
    pesagens = Pesagem.get_pesagem()
    return render_template("pesagens.html", pesagens = pesagens)
