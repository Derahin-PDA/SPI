from spi_master import SPI_Master
from machine import Pin, SPI
from utime import sleep_ms
import array

#SPI
master = SPI_Master(mosi_pin=11, miso_pin=12, sck_pin=10, csel_pin=13, spi_words=1, F_SPI=1_000_000)


#SPI
cs = Pin(5)
spi = SPI(1,
          baudrate=1000000,
          polarity=0,
          phase=0,
          sck = Pin(2),
          mosi = Pin(3),
          miso = Pin(4))
#SD
sd = SDCard(spi, cs)
vol = VfsFat(sd)
mount(vol, "/sd")

cont = 0


#Recopilar datos
for ruta in listdir("/sd"):
    if cont >= 14:
        break
    if ruta[:7] == "Alertas":
        archivo = open("/sd/"+ruta, "r")
        aux = archivo.read()
        archivo.close()

        cruces = 0

        for linea in aux.split("\n"):
            if linea == "":
                continue
            cruces += int(linea[:2])
        
        datos.insert(0,cruces)
        cont += 1


def leer():
    try:
        with open('Alertas.txt', 'r') as file:
            lineas = file.readlines()
            datos = [linea.split(':')[-1].strip() for linea in lineas]  # Utiliza list comprehension para obtener los números
            return datos
    except FileNotFoundError:
        print("El archivo 'Alertas.txt' no se encontró.")
        return []  # Devuelve una lista vacía en caso de error
    except Exception as e:
        print("Ocurrió un error al intentar leer el archivo:", str(e))
        return []  # Devuelve una lista vacía en caso de error
    
alertas = leer() #Lista de datos a enviar
TERMINAR = "&&&&" #Palabra de 4 caracteres para terminar la conexión


#sync
inicio = Pin(18,Pin.IN)
while inicio.value() == 0:
    sleep_ms(1)

#eviar datos
for alerta in alertas:
    paquete = array.array("I", [int("0x"+"{:04d}".format(int(alerta)).encode("utf-8").hex())])
    master.write(paquete)
    sleep_ms(100)

paquete = array.array("I", [int("0x"+TERMINAR.encode("utf-8").hex())])
master.write(paquete)

print("Terminar conexion")
print(alertas)