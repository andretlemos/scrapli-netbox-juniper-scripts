from scrapli.driver.core import AsyncJunosDriver
from getpass import getpass
import pynetbox
from rich import print
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

nb_url = os.getenv("NETBOX_URL")
nb_token = os.getenv("NETBOX_TOKEN")

username = input("Digite o seu nome de usuario: ")
passwd = getpass("Digite seua senha: ")
#command = "show version"
command = input("Digite o comando a ser enviado: ")

parametros_comuns = {
    "auth_username": username,
    "auth_password": passwd,
    "auth_strict_key": False,
    "transport": "asyncssh",
    }

#router = input("Digite o roteador para coletar as informacoes: ").upper()
#command = open("commands.txt", "r")
nb = pynetbox.api(nb_url,token=nb_token, threading=True)
devices = nb.dcim.devices.filter(role="core", status="active")

routers = {}


async def connect_and_execute(router):
    router_ip = routers[router]
    device =  {"host": router_ip, **parametros_comuns }
    async with AsyncJunosDriver(**device) as conn:
        response = await conn.send_command(command)
        print(f"### Enviando o comando para o roteador { router } ####\n ")
        print(response.result)

async def main():

    for device in devices:
        if str(device.tags) == "[CORE]":
            ip = str(device.primary_ip)
            ip = ip.split("/")[0]
            router = device.name
           #Adicionando o nome do roteador com seu ip no dicionário
            routers[router] = ip

    tasks = [connect_and_execute(router) for router in routers]
    try:
        await asyncio.gather(*tasks)
    except:
        print(f"Não foi possível acessar o roteador {router}")

if __name__ == "__main__":
    asyncio.run(main())
