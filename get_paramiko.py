#!/usr/bin/python3

# Importamos los módulos a utilizar
import paramiko
import time


# Definimos la función para enviar comandos
def enviar_comandos(conexion, comando):
    conexion.send(comando + "\n")
    time.sleep(1)


# Definimos la función para recibir la salida
def recibir_salida(conexion):
    return conexion.recv(65535).decode("utf-8")


# Definimos nuestro inventario de equipos y comandos a utilizar
inventario = {
    "R1": "show version",
    "R2": "show interface status",
}


for equipos, comando in inventario.items():
    parametro_conexion = paramiko.SSHClient()
    parametro_conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    parametro_conexion.connect(
        hostname=equipos,
        port=22,
        username="cisco",
        password="cisco",
        look_for_keys=False,
        allow_agent=False,
    )

    conexion = parametro_conexion.invoke_shell()
    time.sleep(1)
    print(f"Ingresando en {recibir_salida(conexion).strip()} sastifactoriamente")

    comandos = [
        "terminal length 0",
        "show vlan brief",
        comando,
    ]

    for comando in comandos:
        enviar_comandos(conexion, comando)
        print(recibir_salida(conexion))

    conexion.close()
