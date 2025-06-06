from flask import Flask, Blueprint, render_template, request,redirect, url_for,jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from utils.create_db import create_db
import json
from models.db import db, instance
from controllers.pesagem_controller import pesagem_, Pesagem

def create_app():
    app = Flask(__name__, template_folder="../views/", static_folder="../static/")

    # BLUEPRINTS
    app.register_blueprint(pesagem_, url_prefix='/')

    # VARIÁVEIS GLOBAIS
    topic_subscribe1 = "exp.criativas/espparapc"
    topic_subscribe2 = "exp.criativas/pcparaesp"

    app.ids_vacas = []
    app.pesagens = []
    app.data_horas = []

    # CONFIGURAÇÕES MQTT
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance

    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template("home.html")

    @app.route('/tempo_real')
    def tempo_real():

        return render_template("tempo_real.html", ids_vacas = app.ids_vacas, pesagens = app.pesagens, data_horas = app.data_horas)
    
    @app.route('/publish_message', methods=['GET','POST'])
    def publish_message():
        request_data = request.get_json()
        publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
        return jsonify(publish_result)

    @app.route('/abrir', methods=['GET','POST'])
    def publish_abrir():
        dispositivo = request.form.get('abrir')
        acao = "abrir"
        mensagem = {
            "dispositivo": dispositivo,
            "acao": acao
        }

        mqtt_client.publish(topic_subscribe2, json.dumps(mensagem))
        return redirect(url_for('tempo_real'))

    @app.route('/fechar', methods=['GET','POST'])
    def publish_fechar():
        dispositivo = request.form.get('fechar')
        acao = "fechar"
        mensagem = {
            "dispositivo": dispositivo,
            "acao": acao
        }

        mqtt_client.publish(topic_subscribe2, json.dumps(mensagem))
        return redirect(url_for('tempo_real'))

    # MÉTODOS MQTT
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe1) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")


    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global ids_vacas, pesagens, data_horas
        js = json.loads(message.payload.decode())
        id = None
        valor = None
        data_hora = None
        for key, value in js.items():
            if key == "id_vaca":
                id = value
            elif key == "pesagem":
                valor = value
            elif key == "data_hora":
                data_hora = value
        if id and valor and data_hora:
            app.ids_vacas.append(id)
            app.pesagens.append(valor)
            app.data_horas.append(data_hora)
            with app.app_context():
                Pesagem.save_pesagem(data_hora, valor, id)

    
    return app

