#!/usr/bin/env python
# -*- coding: utf-8 -*-
from obswebsocket import obsws, requests, exceptions, events
import logging
import time

from obswebsocket.base_classes import Baserequests
import websocket

# cambiar
config = {
    "PASSWORD_SERVIDOR_WS_OBS": "12345", # Contraseña configuracion del servidor websocket
    "IP_SERVIDOR_WS_OBS": "localhost",
    "PUERTO_SERVIDOR_WS_OBS": 4444,
    "pantalla1": "nombre_pantalla1",
    "pantalla2": "nombre_pantalla2",
    "pantalla3": "nombre_pantalla3"
}

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

            textoInput.append("\n0) Salir\n\nElige pantalla cambiar: ")
            textoInput = "".join(textoInput)
            indexNextScene = int(input(textoInput)) - 1

            if indexNextScene == -1:
                salir = True
                break

            if listScenes[indexNextScene]["name"] == nameCurrentScene:
                continue

            clientWs.call(requests.SetCurrentScene(listScenes[indexNextScene]["name"]))

        except KeyboardInterrupt:
            logging.error("error keyboard")
            time.sleep(2)
        except exceptions.ConnectionFailure:
            logging.error("Fallo conexion. ¿Contraseña Mal? / ¿No iniciado OBS? / ¿Reconexion?")
            time.sleep(2)
        except websocket.WebSocketConnectionClosedException:
            logging.error("OBS Ha Desconectado")
            time.sleep(2)
            # conexionError(clientWs)

        # for currentScene in listScenes:
            # sceneName = currentScene['name']
            # if (currentScene["name"] == config["pantalla1"]):

            # print(u"Switching to {}".format(sceneName))
            # clientWs.call(requests.SetCurrentScene(sceneName))
            
            # time.sleep(2)

        #     for currentSource in fuentes.getSources():
        #     # for f in s["sources"]:
        #         sourceName = currentSource['name']
        #         print(u"Switching to {}".format(sourceName))
        #         getInfo: Baserequests = clientWs.call(requests.GetSceneItemProperties(currentSource))
        #         if "visible" not in getInfo.datain:
        #             continue
        #         visibleToggle = getInfo.getVisible()
        #         visibleToggle = not visibleToggle
        #         p = requests.SetSceneItemProperties(item=currentSource, visible=visibleToggle)
        #         clientWs.call( p)

        # print("End of list")

  
        
# def conexionError(clientWs: obsws):

#     for i in range(0, 15):
#         try:
#             reconnecting = True
#             clientWs.reconnect()
#             time.sleep(2)
#             if clientWs.ws.connected == True:
#                 break

#         except KeyboardInterrupt:
#             logging.error("error keyboard")
#         except exceptions.ConnectionFailure:
#             logging.error("Fallo conexion. ¿Contraseña Mal? / ¿No iniciado OBS? / ¿Reconexion?")
#         except websocket.WebSocketConnectionClosedException:
#             logging.error("OBS Ha Desconectado")
#             time.sleep(2)
#             conexionError(clientWs)

#     if clientWs.ws.connected == True:
#         main()


if __name__ == '__main__':
    main()