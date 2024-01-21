from spi_slave import SPI_Slave
from machine import Pin
from utime import sleep_ms
import ssd1306
import time
import utime

TERMINAR = "&&&&" #Palabra de 4 caracteres para terminar la conexión

# Inicializar componentes
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

# Variables globales
ciclo = 2
tiempo = time.time()
lista = []

#Leer dato
def Leer_SPI():
    read = slave.rx_words()
    write = slave.tx_words()
    write[0] = read[0]
    
    try:
        dato = read[0].to_bytes(4, "big").decode("utf-8")
    except:
        return "saltar"
    
    slave.put_words()
    
    return dato

#SPI
slave = SPI_Slave(csel=28, mosi=26, sck=27, miso=22, spi_words=1, F_PIO=10_000_000)
slave.put_words()

fin = False
datos = []

#sync
inicio = Pin(13,Pin.OUT)
inicio.value(1)
sleep_ms(10)
inicio.value(0)


def formato_grafica(alertas):
    global tiempo, lista, X_prev, Y_prev  # Declarar variables globales

    # Limpiar la pantalla OLED
    oled.fill(0)

    # Obtener la fecha y hora actuales
    current_time = time.localtime()
    template_fecha = "{:02d}/{:02d}/{:04d}".format(current_time[2], current_time[1], current_time[0])
    template_hora = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])

    # Mostrar la fecha y hora en la pantalla OLED
    oled.text(template_fecha, 0, 0)
    oled.text(template_hora, 0, 9)
    oled.hline(0, 16, 128, 1)  # Línea divisoria

    # Verificar si es tiempo de actualizar la lista y la gráfica
    
    #if tiempo + ciclo < time.time():
    lista.insert(0, alertas)  # Agregar alerta a la lista
    tiempo = time.time()  # Actualizar el tiempo
    for k in range(len(lista)):
        X = 132 - (k + 1) * 8
        Y = int(60 - lista[k] * 5) if tiempo + ciclo < time.time() else int(60 - lista[k])
        oled.pixel(X, Y, 1)  # Dibujar píxel en la pantalla OLED
        if k > 0:
            oled.line(X_prev, Y_prev, X, Y, 1)  # Dibujar línea entre píxeles
        X_prev, Y_prev = X, Y

    oled.show()  # Mostrar cambios en la pantalla OLED


#receptor datos
while True:
    if slave.received():
        dato = Leer_SPI()
        if dato == TERMINAR:
            break
        else:
            datos.append(int(dato))
            
for dato in datos:
    formato_grafica(dato)

print("Terminar conexion")
