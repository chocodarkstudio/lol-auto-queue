import pygetwindow
import pyautogui
import winsound

class WindowsHelper:
    @staticmethod
    def play_sound(file_path):
        winsound.PlaySound(file_path, flags=winsound.SND_ASYNC)

    @staticmethod
    def is_client_opened():
        try:
            results = pygetwindow.getWindowsWithTitle('League of Legends')
            return results is not None and len(results) > 0
        except IndexError:
            return False
        finally:
            return True

    @staticmethod
    def is_game_opened():
        try:
            results = pygetwindow.getWindowsWithTitle('League of Legends')
            return results is not None and len(results) > 1
        except IndexError:
            return False
        finally:
            return True

    @staticmethod
    def center_lol_window():
        try:
            w = pygetwindow.getWindowsWithTitle('League of Legends')[0]
            #w.restore() # restore window if its minimized
            w.moveTo(40, 10) # move window to 40, 10
        except IndexError:
            #print("list index out of range (Quiza el lol no este abierto)")
            pass

    @staticmethod
    def focus_lol_window():
        try:
            w = pygetwindow.getWindowsWithTitle('League of Legends')[0]
            #w.restore() # restore window if its minimized
            w.activate()
        except IndexError:
            #print("list index out of range (Quiza el lol no este abierto)")
            pass

    @staticmethod
    def is_img_in_screen(file_path, _confidence=0.7):
        box = pyautogui.locateOnScreen(file_path, confidence=_confidence)
        return box is not None

    # return true on success
    @staticmethod
    def click_img(file_path, _confidence=0.7, _duration=0.2):
        box = pyautogui.locateCenterOnScreen(file_path, confidence=_confidence)
        
        if box is not None:
            x, y = box
            pyautogui.click(x, y, duration=_duration)
            return True
        return False

    @staticmethod
    def press(key, presses=1):
        pyautogui.press(key, presses)

    @staticmethod
    def write(text, interval=0.01):
        pyautogui.write(text, interval)

    @staticmethod
    def click(x,y, duration=0.0, clicks=1):
        pyautogui.click(x,y, duration=duration, clicks=clicks)

    @staticmethod
    def get_lane():
        lanes = ["imgs/lane_top.png", "imgs/lane_jungle.png",
                 "imgs/lane_mid.png", "imgs/lane_adc.png", "imgs/lane_sup.png"]

        # repeat this twice to make sure get the lane
        # the loop breaks until a lane is obtained, so if no lane was detected, repeat it again
        for rep in range(0, 1):

            me_box = pyautogui.locateCenterOnScreen("imgs/champ_selection.png", confidence=0.9)
            if me_box is not None:
                me_x, me_y = me_box
                for lane in lanes:
                    lane_box = pyautogui.locateCenterOnScreen(lane, confidence=0.9)
                    if lane_box is not None:
                        x, y = lane_box
                        distance = abs(y-me_y)
                        if distance <= 20:
                            # removes the ".png" text
                            return lane[:-4]
        return None
