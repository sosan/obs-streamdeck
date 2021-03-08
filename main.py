#!/usr/bin/env python
# -*- coding: utf-8 -*-
from obswebsocket import obsws, requests, exceptions, events
from obswebsocket.base_classes import Baserequests
import websocket
import logging
import time


# cambiar
config = {
    "PASSWORD_SERVIDOR_WS_OBS": "12345", # Contraseña configuracion del servidor websocket
    "IP_SERVIDOR_WS_OBS": "localhost",
    "PUERTO_SERVIDOR_WS_OBS": 4444,
    "pantalla1": "nombre_pantalla1",
    "pantalla2": "nombre_pantalla2",
    "pantalla3": "nombre_pantalla3"
}

def checkings(indexNextScene, listScenes, nameCurrentScene):
    # introducido un digito mayor al listado de escenas
    if indexNextScene > len(listScenes):
        logging.info("Digito mayor al numero de escenas")
        return False

    # digito inferiro a 0
    if indexNextScene < 0:
        logging.info("Digito inferior a 0")
        return False

    # escena actual
    if listScenes[indexNextScene]["name"] == nameCurrentScene:
        return False

    return True

def main():
    clientWs = obsws(
        config["IP_SERVIDOR_WS_OBS"],
        config["PUERTO_SERVIDOR_WS_OBS"],
        config["PASSWORD_SERVIDOR_WS_OBS"]
    )

    salir = False
    while salir == False:
        try:

            if clientWs.ws == None or clientWs.ws.connected == False:
                clientWs.connect()

            scenes = clientWs.call(requests.GetSceneList())
            fuentes: Baserequests = clientWs.call(requests.GetSourcesList())

            getInfoCurrentScene = clientWs.call(requests.GetCurrentScene())
            nameCurrentScene = getInfoCurrentScene.datain["name"]
            textoInput: list = [ "\n" ]
            listScenes = scenes.getScenes()
            for i in range(0, len(listScenes)):
                currentName = listScenes[i]["name"]
                if (currentName == nameCurrentScene):
                    textoInput.append("\n{}) {} <<< Actual".format(i + 1, currentName ) )
                else:
                    textoInput.append("\n{}) {}".format(i + 1, currentName ) )

            textoInput.append("\n\n0) Salir\n\nElige pantalla cambiar: ")
            textoInput = "".join(textoInput)
            rawInput: str = input(textoInput)
            if str.isdigit(rawInput) == False:
                continue
            indexNextScene = int(rawInput) - 1

            # salir
            if indexNextScene == -1:
                salir = True
                clientWs.disconnect()
                break

            # comprobaciones digitos
            if checkings(indexNextScene, listScenes, nameCurrentScene) == False:
                continue

            # cambio de escena
            clientWs.call(requests.SetCurrentScene(listScenes[indexNextScene]["name"]))

        except exceptions.ConnectionFailure:
            logging.error("Fallo conexion. ¿Contraseña Mal? / ¿No iniciado OBS? / ¿Reconexion?")
            time.sleep(2)
        except websocket.WebSocketConnectionClosedException:
            logging.error("OBS Ha Desconectado")
            time.sleep(2)
        except ValueError:
            logging.error("Caracter no permitido")

if __name__ == '__main__':
    main()