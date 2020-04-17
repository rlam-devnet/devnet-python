#!/usr/bin/python3

# Importamos los módulos a utilizar
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from yaml import safe_load
import time


# Leemos nuestro archivo con estructura YML para el inventario
with open("hosts.yml", "r") as handle:
    host_root = safe_load(handle)

# Realizamos el mapa del uso de versiones de ios o iosxr
mapa_plataforma = {"ios": "cisco_ios", "iosxr": "cisco_xr"}


# Interactuamos sobre la lista de host cargada
for host in host_root["lista_host"]:

    platform = mapa_plataforma[host["platform"]]
    # cargamos el host especifico en la declaración de arhcivo
    with open(f"vars/{host['name']}_conf.yml", "r") as handle:
        ntps = safe_load(handle)


# Configuramos el entorno de jinja2
j2_env = Environment(
    loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
)
template = j2_env.get_template(
    f"templates/netmiko/{platform}_conf.j2"
)
new_ntp_config = template.render(data=ntps)

# Creamos la conexion con Netmiko
conexion = Netmiko(
    host=host["name"],
    username="xxx",
    password="xxx",
    device_type=platform,
)

print(f"Ingresando dentro {conexion.find_prompt()} Satisfactoriamente")

resultado = conexion.send_config_set(new_ntp_config.split("\n"))

print(resultado)

conexion.disconnect()
