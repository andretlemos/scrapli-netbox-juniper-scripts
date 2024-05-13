from scrapli.driver.core import JunosDriver
from rich import print
from getpass import getpass
import pynetbox
import os
from dotenv import load_dotenv

load_dotenv()

nb_url = os.getenv("NETBOX_URL")
nb_token = os.getenv("NETBOX_TOKEN")nb_url = os.

username = input("Digite o seu nome de usuario: ")
passwd = getpass("Digite seua senha: ")
roteador = input("Digite o roteador conforme nome no netbox: ")
command = input("Digite o comando:" )

nb = pynetbox.api(nb_url,token=nb_token, threading=True)


device = nb.dcim.devices.get(name=roteador)

ip  = device.primary_ip
ip  = str(device.primary_ip)
ip = ip.split("/")[0]


my_device = { "host": ip,"auth_username": username,"auth_password": passwd,"auth_strict_key": False,}

with JunosDriver(**my_device) as conn:
        response = conn.send_command(command)
        print(response.result)
