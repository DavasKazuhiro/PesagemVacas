from flask import Flask, render_template, request,redirect, url_for,jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

ids_vacas = []
pesagens = []
data_horas = []

atuadores_values= 1

app= Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

mqtt_client= Mqtt()
mqtt_client.init_app(app)

topic_subscribe1 = "exp.criativas/espparapc"
topic_subscribe2 = "exp.criativas/pcparaesp"


@app.route('/tempo_real')
def tempo_real():
    global ids_vacas, pesagens, data_horas
    return render_template("tempo_real.html", ids_vacas = ids_vacas, pesagens = pesagens, data_horas = data_horas)

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
    for key, value in js.items():
        if key == "id_vaca":
            ids_vacas.append(value)
        elif key == "pesagem":
            pesagens.append(value)
        elif key == "data_hora":
            data_horas.append(value)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) 