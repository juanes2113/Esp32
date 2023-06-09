from machine import Pin, ADC
import time

print('Sistema de seguridad anti-incendios')

LDR = ADC(Pin(34)) # LDR = sensor de luz, ADC = conversor analógico-digital
led = Pin(18, Pin.OUT)
LM35_pin = Pin(35)
adc = ADC(LM35_pin)

# Rango de temperatura
adc.atten(ADC.ATTN_11DB)

# Función para convertir el valor ADC en °C
def adc_a_temperatura_celsius(adc_valor):
    return (adc_valor * 3.3 / 4095) * 100

# Función de grados °C a °F
def celsius_a_fahrenheit(temp_celsius):
    return temp_celsius * 9 / 5 + 32

print('Valor de la resistencia')

while True:
    LDR_value = LDR.read() # Leyendo la intensidad de la luz
    if LDR_value < 300: # Entre menor sea el valor, más hay que tapar el sensor
        led.value(1)
    else:
        led.value(0)
    print("Valor del LDR:", LDR_value)
    #sleep(1) # Muestrea cada 1 segundo

    adc_valor = adc.read()
    temp_celsius = adc_a_temperatura_celsius(adc_valor)
    temp_fahrenheit = celsius_a_fahrenheit(temp_celsius)
    print('Temperatura: {:.2f}°C ~ {:.2f}°F'.format(temp_celsius, temp_fahrenheit))
    time.sleep(1)
