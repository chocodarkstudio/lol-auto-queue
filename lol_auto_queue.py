from __future__ import annotations

import time
import winsound

from windows_helper import *
from tray_icon import *
from spelling_corrector import *
from classic_queue import *
from settings import *

# Project creation Date: 14/07/2021
# 1st Updated at: 16/06/2022 (py v3.6)
# 2nd Updated at: 24/04/2024 (py v3.10)

# TODO:
# hacer que el sistema detecte si se salteo alguna fase en el lol y sincronizarlo
# hacer interface para seleccionar campeones con una lista de los nombres de todos los campeones
# usar la api de lol para saber que campeones tiene el jugador y asi saber si se puede elegir el que el quiere
# detectar que linea te ha tocado y elegir campeon en base a eso
# hacer un modo para partidas ocultas (que escribe en el chat "top") etc
# hacer que banee un campeon y eliga uno (ojo con que se haya baneado el champ o que tu compa lo tenga y lo quieras banear)
# evitar descargar siempre 'all_champions.json' y free champs

# Partial solved:
# si se mueve la ventana no puede hacer clicks correctos -> Se arreglo centrando la ventana

# Solved:
# usar config.json
# agregar strayicon
# agregar al icon una opcion para abrir lol y el poro

# Info:
# 8 segundos masomenos dura la pantalla de aceptar partida


def play_sound(file_path):
    winsound.PlaySound(file_path, flags=winsound.SND_ASYNC)


def img_path(file_path):
    return Resolutions.img_path + "/" + file_path



# this is the StateMachine
class LolAutoMatch:
    def __init__(self, icon: TrayIcon):
        self.icon: TrayIcon = icon

        self.all_champs: dict[str, str] = {}
        # self.all_champs = LolApi.get_all_champions()

        self.free_champs: list[str] = []
        # self.free_champs = LolApi.get_free_champions(self.get_free_champions())

        #print("All Champs", self.all_champs)
        print("Free Champs", self.free_champs)


        self.champs_to_play: list[str] = None
        self.champs_to_block: list[str] = None

        self.set_champs(
            Config.get("champs_to_play"),
            Config.get("champs_to_block")
        )

        # create queue machine
        self.classicQueue = ClassicQueueMachine(self.champs_to_play, self.champs_to_block)
        self.classicQueue.on_change_state_callback = self.on_change_state
        self.classicQueue.evaluate_all()

        play_sound("audio/waiting.wav")


    def set_champs(self, champs_to_play=None, champs_to_block=None):
        if champs_to_play is None:
            champs_to_play = []
        if champs_to_block is None:
            champs_to_block = []

        if len(champs_to_play) > 0:
            self.champs_to_play = champs_to_play

        if len(champs_to_block) > 0:
            self.champs_to_block = champs_to_block

        print(f"Campeones a jugar: {self.champs_to_play} \nCampeones a banear: {self.champs_to_block}")

    def update_tray_icon(self):
        # no icon
        if self.icon is not None:
            return

        # game is not opened
        if not WindowsHelper.is_client_opened():
            #self.icon.add_option("Abrir lol", self.icon.open_league_of_legends)
            self.icon.set_icon("icons/default.ico")

        # in queue or accepting match
        elif type(self.classicQueue.current_state) in (InQState, MatchFoundState):
            self.icon.set_icon("searching.ico")

        # 
        elif type(self.classicQueue.current_state) in (BlockChampState, LockChampState):
            self.icon.set_icon("icons/champ_selection.ico")

    def on_change_state(self):
        self.update_tray_icon()

    def update_state(self):
        self.classicQueue.update_state()
        self.classicQueue.evaluate_all()
      

if __name__ == "__main__":
    icon = TrayIcon()
    match = LolAutoMatch(icon)

    #champsCorrector = SpellingCorrector(list(match.all_champs))
    #inp_champ = input("\nEscribe que campeon jugaras_ ")
    #match.set_champs(champsCorrector.get(inp_champ))

    # if icon is alive update states
    while match.icon.is_running():
        match.update_state()
        time.sleep(0.5)
