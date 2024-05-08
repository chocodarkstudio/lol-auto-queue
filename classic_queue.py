from __future__ import annotations
from state_machine import State, StateMachine
from windows_helper import WindowsHelper
import time
from settings import Resolutions

def img_path(file_path):
    return Resolutions.img_path + "/" + file_path


class InQState(State):
    def get_name(self):
        return "InQState"

    @classmethod
    def evaluate(cls, context: ClassicQueueMachine):
        # first evaluate the base class
        if super().evaluate(context):
            return True
        
        # 'InQ' image is in the background but is actually the 'MatchFound' screen (Fake positive)
        if type(context.current_state) == MatchFoundState and WindowsHelper.is_img_in_screen(img_path("cannot_accept_match.png"), _confidence=0.5):
            return False
        
        return WindowsHelper.is_img_in_screen(img_path("inQ.png"))
    
    def on_enter(self, context: ClassicQueueMachine):
        super().on_enter(context)
        print("In Queue")

        # back to queue
        if context.inMatch:
            WindowsHelper.play_sound("audio/canceled.wav")

        context.inMatch = False

    def on_update(self, context: ClassicQueueMachine):
        super().on_update(context)
        #print("In Queue")


class MatchFoundState(State):
    def get_name(self):
        return "MatchFoundState"

    @classmethod
    def evaluate(cls, context: ClassicQueueMachine):
        # first evaluate the base class
        if super().evaluate(context):
            return True

        return WindowsHelper.is_img_in_screen(img_path("accept_match.png"))
    
    def on_enter(self, context: ClassicQueueMachine):
        super().on_enter(context)
        print("Partida encontrada")

        # accept match in 5s
        self.timer = 5

    def on_update(self, context: ClassicQueueMachine):
        super().on_update(context)

        self.timer -= 1
        if self.timer > 0:
            print(f"Aceptando en {self.timer}s")
            WindowsHelper.play_sound("audio/waiting.wav")

        # only if timer its 0, negative dosnt count
        elif self.timer == 0:
            self.accept_match(context)

        time.sleep(0.5)
    
    def accept_match(self, context: ClassicQueueMachine):
        WindowsHelper.focus_lol_window()
        time.sleep(0.1)

        WindowsHelper.click_img(img_path("accept_match.png"))
        WindowsHelper.play_sound("audio/acepted.wav")
        print("Partida aceptada")

        # wait until the match has been accepted
        time.sleep(1)

        context.inMatch = True


class BlockChampState(State):
    def get_name(self):
        return "BlockChampState"

    @classmethod
    def evaluate(cls, context: ClassicQueueMachine):
        # first evaluate the base class
        if super().evaluate(context):
            return True

        if not context.inMatch:
            return False

        return WindowsHelper.is_img_in_screen(img_path("cannot_block_button.png"), 0.9)
    
    def on_enter(self, context: ClassicQueueMachine):
        super().on_enter(context)
        print("Bloqueando campeon")

        self.champBlocked = False
        self.champIndex = 0


    def on_update(self, context: ClassicQueueMachine):
        super().on_update(context)

        # champ is already blocked
        if self.champBlocked:
            return

        # index out of bounds
        if self.champIndex >= len(context.champs_to_block):
            print("Imposible bloquear un campeon :(")
            return

        champName = context.champs_to_block[self.champIndex]
        clicked = WindowsHelper.click_img(img_path("search_champ.png"))

        # cannot click on search champ button
        if not clicked:
            return

        self.champIndex += 1

        # write champ name
        WindowsHelper.press("backspace", presses=20)
        WindowsHelper.write(champName, interval=0.01)

        # wait until it search and load champ list
        time.sleep(3)

        # click on the champ
        WindowsHelper.click(430, 150, duration=0.5)
        #time.sleep(2)
        
        #self.click_img("block_champ.png")

        self.champBlocked = True


class LockChampState(State):
    def get_name(self):
        return "LockChampState"

    @classmethod
    def evaluate(cls, context: ClassicQueueMachine):
        # first evaluate the base class
        if super().evaluate(context):
            return True
        
        if not context.inMatch:
            return False

        return WindowsHelper.is_img_in_screen(img_path("cannot_lock_champ.png"), 0.9) or WindowsHelper.is_img_in_screen(img_path("lock_champ.png"))
    
    def on_enter(self, context: ClassicQueueMachine):
        super().on_enter(context)

        self.champLocked = False
        self.champIndex = 0

    def on_update(self, context: ClassicQueueMachine):
        super().on_update(context)

        # champ is already locked
        if self.champLocked:
            return

        # index out of bounds
        if self.champIndex >= len(context.champs_to_play):
            print("Imposible seleccionar un campeon :(")
            WindowsHelper.play_sound("audio/no_champ_alert.wav")
            return
        
        champName = context.champs_to_play[self.champIndex]
        clicked = WindowsHelper.click_img(img_path("search_champ.png"))

        # cannot click on search champ button
        if not clicked:
            return

        print(f"Lock champ: {champName}")

        # write champ name
        WindowsHelper.press("backspace", presses=20)
        WindowsHelper.write(champName, interval=0.01)

        # wait until it search and load champ list
        time.sleep(2)

        # click on the champ
        WindowsHelper.click(430, 150, duration=0.5)
        time.sleep(1)

        # lock champ in 4s
        timer = 4
        for i in range(0, timer):
            print(f"Lock en {timer - i}s")
            time.sleep(1)
            if not WindowsHelper.is_img_in_screen(img_path("lock_champ.png"), _confidence=0.8):
                print("No se puede seleccionar el campeon")
                break
        
        # next champ index
        self.champIndex += 1

        if WindowsHelper.click_img(img_path("lock_champ.png")):
            print(f"Champ locked: {champName}")
            self.champLocked = True


class InGameState(State):
    def get_name(self):
        return "InGameState"

    @classmethod
    def evaluate(cls, context: ClassicQueueMachine):
        # first evaluate the base class
        if super().evaluate(context):
            return True
        
        if not context.inMatch:
            return False
        
        # only if last state is lock champ
        #if type(context.current_state) is not LockChampState:
        #    return False

        return WindowsHelper.is_game_opened()
    
    def on_enter(self, context: ClassicQueueMachine):
        super().on_enter(context)
        print("La partida ha iniciado")

    def on_update(self, context: ClassicQueueMachine):
        super().on_update(context)


class ClassicQueueMachine(StateMachine):
    def __init__(self, champs_to_play:list[str], champs_to_block:list[str]):
        super().__init__()
        self.state_list = [InQState(), MatchFoundState(), BlockChampState(), LockChampState()]
        
        self.inMatch = False

        self.champs_to_play = champs_to_play
        self.champs_to_block = champs_to_block


if __name__ == '__main__':
    classicQueue = ClassicQueueMachine(["lee"],[])
    classicQueue.evaluate_all()

    while True:
        classicQueue.update_state()
        classicQueue.evaluate_all()
        time.sleep(0.5)