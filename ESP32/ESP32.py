import machine
import network
import time
import urequests

# Configuración de la conexión WiFi
WIFI_SSID = "iPhone de Juan Pablo"
WIFI_PASSWORD = "holap1234"

# Configuración del servidor ThingSpeak
THINGSPEAK_WRITE_API_KEY = "ZBXGP5FAZDGTLOCW"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# Configuración del pin GPIO para el LDR - Sensor de luz
LDR_PIN = 34

# Configuración del pin GPIO para el LED - Pin de salida para el sensor de luz
LED_PIN = 18
led = machine.Pin(LED_PIN, machine.Pin.OUT)

# Configuración del pin GPIO para el LED - Pin de salida para el sensor de temperatura
LED_PIN_2 = 19
led_2 = machine.Pin(LED_PIN_2, machine.Pin.OUT)

# Configuración del pin GPIO para la BOMBA - Pin de salida
BOMB_PIN = 23
bomba = machine.Pin(BOMB_PIN, machine.Pin.OUT)
bomba.off()

# Configuración del pin GPIO para el MQ2 - Sensor de gas
MQ2_PIN = 32
mq2 = machine.Pin(MQ2_PIN, machine.Pin.IN)

# Configuración del pin GPIO para el LM35 - Sensor de tempetarura
LM35_PIN = 35
adc = machine.ADC(machine.Pin(LM35_PIN)) # ADC Conversor analogo digital
adc.atten(machine.ADC.ATTN_11DB) # Frecuencia de 11 decibeles
adc.width(machine.ADC.WIDTH_12BIT) # <=12 bit

# Conexión a la red WiFi
def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('Conectándose a la red WiFi...')
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wifi.isconnected():
            pass
    print('Conexión WiFi establecida!')
    print('Dirección IP:', wifi.ifconfig()[0])

# Lectura del sensor LDR
def read_ldr():
    ldr = machine.ADC(machine.Pin(LDR_PIN)) # ldr se convierte una señal digital
    ldr_value = ldr.read()
    return ldr_value

# Encendido del LED si la lectura del LDR es menor a 300- Fotoresistor
def led_control(ldr_value):
    print("Valor del LDR:", ldr_value)
    if ldr_value < 1500: # 300 resistencia
        led.on()
    else:
        led.off()

# Lectura del sensor LM35 - Sensor de tempetarura
def read_lm35():
    lm35_value = adc.read()
    return (lm35_value * 3.3 / 4095) * 100 # lm35_value recibe un valor de voltaje y lo convertimos a °C

# Controlador de temperatura
def temperaturecontroller(lm35_value):
    print('Temperatura: ', lm35_value)
    if lm35_value >= 20 and lm35_value <= 24:
        led_2.on()
        bomba.off()
    elif lm35_value > 47:
        led_2.on()
        bomba.on()
    else:
        led_2.off()
        bomba.off()

# Lectura del sensor MQ2
def read_mq2():
    mq2_value = mq2.value()
    return mq2_value

# Controlador de humo
def smokecontroller(mq2_value):
    print('MQ2:', mq2_value)
    if mq2_value == 0:
        led_2.on()
        bomba.on()
    else:
        led_2.off()
        bomba.off()

# Envío de datos a ThingSpeak
def send_data_to_thingspeak(ldr_value, lm35_value, mq2_value):
    url = THINGSPEAK_URL + "?key=" + THINGSPEAK_WRITE_API_KEY + "&field1=" + str(ldr_value) + "&field2=" + str(lm35_value) + "&field3=" + str(mq2_value)
    response = urequests.get(url)
    print('Respuesta del servidor:', response.text)

# Conexión a la red WiFi
connect_to_wifi()

# Bucle principal
while True:
    # Lectura del sensor LDR
    ldr_value = read_ldr()
    # Encendido del LED si la lectura del LDR es menor a 150
    led_control(ldr_value)
    # Lectura del sensor LM35
    lm35_value = read_lm35()
    # Controlador de temperatura
    temperaturecontroller(lm35_value)
    # Lectura del sensor MQ2
    mq2_value = read_mq2()
    # Controlador de humo
    smokecontroller(mq2_value)
    # Envío de datos a ThingSpeak
    send_data_to_thingspeak(ldr_value, lm35_value, mq2_value)
    # Espera de 1 segundos
    time.sleep(1)
