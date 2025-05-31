
from utime import sleep_us, time, sleep
from machine import Pin, PWM
from micropython import const
from random import randint
import _thread
import network
from umqtt.simple import MQTTClient
import ujson


#CLASSES BALANÇA

class HX711Exception(Exception):
    pass

class InvalidMode(HX711Exception):
    pass

class DeviceIsNotReady(HX711Exception):
    pass

class HX711(object):
    """
    Micropython driver for Avia Semiconductor's HX711
    24-Bit Analog-to-Digital Converter
    """
    CHANNEL_A_128 = const(1)
    CHANNEL_A_64 = const(3)
    CHANNEL_B_32 = const(2)

    DATA_BITS = const(24)
    MAX_VALUE = const(0x7fffff)
    MIN_VALUE = const(0x800000)
    READY_TIMEOUT_SEC = const(5)
    SLEEP_DELAY_USEC = const(80)

    def __init__(self, d_out: int, pd_sck: int, channel: int = CHANNEL_A_128):
        self.d_out_pin = Pin(d_out, Pin.IN)
        self.pd_sck_pin = Pin(pd_sck, Pin.OUT, value=0)
        self.channel = channel

    def __repr__(self):
        return "HX711 on channel %s, gain=%s" % self.channel

    def _convert_from_twos_complement(self, value: int) -> int:
        """
        Converts a given integer from the two's complement format.
        """
        if value & (1 << (self.DATA_BITS - 1)):
            value -= 1 << self.DATA_BITS
        return value

    def _set_channel(self):
        """
        Input and gain selection is controlled by the
        number of the input PD_SCK pulses
        3 pulses for Channel A with gain 64
        2 pulses for Channel B with gain 32
        1 pulse for Channel A with gain 128
        """
        for i in range(self._channel):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)

    def _wait(self):
        """
        If the HX711 is not ready within READY_TIMEOUT_SEC
        the DeviceIsNotReady exception will be thrown.
        """
        t0 = time()
        while not self.is_ready():
            if time() - t0 > self.READY_TIMEOUT_SEC:
                raise DeviceIsNotReady()

    @property
    def channel(self) -> tuple:
        """
        Get current input channel in a form
        of a tuple (Channel, Gain)
        """
        if self._channel == self.CHANNEL_A_128:
            return 'A', 128
        if self._channel == self.CHANNEL_A_64:
            return 'A', 64
        if self._channel == self.CHANNEL_B_32:
            return 'B', 32

    @channel.setter
    def channel(self, value):
        """
        Set input channel
        HX711.CHANNEL_A_128 - Channel A with gain 128
        HX711.CHANNEL_A_64 - Channel A with gain 64
        HX711.CHANNEL_B_32 - Channel B with gain 32
        """
        if value not in (self.CHANNEL_A_128, self.CHANNEL_A_64, self.CHANNEL_B_32):
            raise InvalidMode('Gain should be one of HX711.CHANNEL_A_128, HX711.CHANNEL_A_64, HX711.CHANNEL_B_32')
        else:
            self._channel = value

         # i edited this row : if  not self.is_ready():  self._wait()      by hamdi ali 

        if  self.is_ready():                                            
            self._wait()

        for i in range(self.DATA_BITS):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)

        self._set_channel()

    def is_ready(self) -> bool:
        """
        When output data is not ready for retrieval,
        digital output pin DOUT is high.
        """
        return self.d_out_pin.value() == 0

    def power_off(self):
        """
        When PD_SCK pin changes from low to high
        and stays at high for longer than 60 us ,
        HX711 enters power down mode.
        """
        self.pd_sck_pin.value(0)
        self.pd_sck_pin.value(1)
        sleep_us(self.SLEEP_DELAY_USEC)

    def power_on(self):
        """
        When PD_SCK returns to low, HX711 will reset
        and enter normal operation mode.
        """
        self.pd_sck_pin.value(0)
        self.channel = self._channel

    def read(self, raw=False):
        """
        Read current value for current channel with current gain.
        if raw is True, the HX711 output will not be converted
        from two's complement format.
        """
        if not self.is_ready():
            self._wait()

        raw_data = 0
        for i in range(self.DATA_BITS):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)
            raw_data = raw_data << 1 | self.d_out_pin.value()
        self._set_channel()

        if raw:
            return raw_data
        else:
            return self._convert_from_twos_complement(raw_data)


#CLASSE SERVO MOTOR

class Servo:
    # these defaults work for the standard TowerPro SG90
    __servo_pwm_freq = 50
    __min_u10_duty = 26 - 0 # offset for correction
    __max_u10_duty = 123- 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001

    def __init__(self, pin):
        self.__initialise(pin)

    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)

    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u10 = self.__angle_to_u10_duty(angle)
        self.__motor.duty(duty_u10)

    def __angle_to_u10_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty

    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)
        self.pin = pin


#FUNÇÕES

def ler_peso(sensor, n=10):
    sensor.power_on()
    sleep(0.5)

    while not sensor.is_ready():
        pass

    valor = sensor.read()
    sleep(0.05)

    return valor / 420

def abrir_portao(servo):
    servo.move(90)

    if servo.pin == pino_entrada:
        print("Entrada Aberta")
    
    elif servo.pin == pino_saida:
        print("Saída Aberta")

def fechar_portao(servo):
    servo.move(0)

    if servo.pin == pino_entrada:
        print("Entrada Fechada")
    
    elif servo.pin == pino_saida:
        print("Saída Fechada")

def conectar_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.1)
    print(" Connected!")
    print("Connecting to MQTT server... ", end="")

def callback(topic, msg):
    print("Mensagem recebida: ", msg.decode()) 

    try:
        dados = ujson.loads(msg)
        dispositivo = dados.get("dispositivo")
        acao = dados.get("acao")

        if acao == "abrir":
            if dispositivo == "entrada":
                abrir_portao(Servo(pin=pino_entrada))
            elif dispositivo == "saida":
                abrir_portao(Servo(pin=pino_saida))
            else:
                print("Ação desconhecida:", acao)

        elif acao == "fechar":
            if dispositivo == "entrada":
                fechar_portao(Servo(pin=pino_entrada))
            elif dispositivo == "saida":
                fechar_portao(Servo(pin=pino_saida))
            else:
                print("Ação desconhecida:", acao)

        else:
            print("Dispositivo desconhecido:", dispositivo)

    except Exception as e:
        print("Erro ao interpretar JSON:", e)

# MQTT Server Parameters
MQTT_CLIENT_ID = "conect_demo15361"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativas/espparapc"
MQTT_TOPIC_RECEIVE = "exp.criativas/pcparaesp" 
MQTT_USER      = "123456"
MQTT_PASSWORD  = "123456"

#PINOS
pino_balanca_dt = 22
pino_balanca_sck = 23

pino_entrada = 19
pino_saida = 18

pino_botao = 21

#EXECUÇÃO
def main():
    conectar_wifi()
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(callback)
    client.connect()
    print("Connected!")
    client.subscribe(MQTT_TOPIC_RECEIVE)

    balanca = HX711(pino_balanca_dt, pino_balanca_sck, 1)
    botao = Pin(pino_botao, Pin.IN, Pin.PULL_UP)

    entrada = Servo(pin=pino_entrada)
    saida = Servo(pin=pino_saida)

    print("Programa Iniciado")
    fechar_portao(saida)

    while True:
        if botao.value() == False:  # valor é 0 quando pressionado (pull-up ativo)
            id_vaca = randint(1, 100)

            print("Leitura Feita! \nID da vaca:", id_vaca)
            fechar_portao(entrada)
            fechar_portao(saida)

            sleep(2)
            peso = ler_peso(balanca)
            data_hora = "30/05"
            print("Peso", peso)

            mensagem = ujson.dumps({
                "id_vaca": id_vaca,
                "pesagem": peso,
                "data_hora": data_hora
            })

            client.publish(MQTT_TOPIC_SEND, mensagem)
            print("Medição Enviada")

            sleep(1)
            abrir_portao(saida)

            while peso != 0:
                peso = ler_peso(balanca)
                sleep(0.1)

            sleep(2)
            print("A vaca saiu da balança (Peso: {})".format(peso))
            fechar_portao(saida)
            abrir_portao(entrada)

        sleep(0.1)
        client.check_msg()
    


main()

