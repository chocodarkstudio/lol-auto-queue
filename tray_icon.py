
from infi.systray import SysTrayIcon
import threading
import os
from settings import Config

class TrayIcon:
    def __init__(self):
        self.systray: SysTrayIcon = None
        self.execution_thread: threading.Thread = None

        self.default_icon_path = "icons/default.ico"
        self.default_hover_text = "lol auto match ON"

        self.menu_options = (
            ("Toggle", None, self.on_double_click),
            ("League Of Legends", None, self.on_open_league_of_legends),
        )

        self.create()


    def create(self):
        # execution thread already created
        if self.is_running():
            return
        
        self.systray = SysTrayIcon(
            self.default_icon_path,
            self.default_hover_text,
            self.menu_options,
            on_quit=self.on_quit_callback,
            default_menu_index=0
        )

        # start new execution thread
        self.execution_thread = threading.Thread(target=self.systray.start, args=(), daemon=True)
        self.execution_thread.start()


    def close(self):
        # trayIcon not created
        if not self.is_running():
            return

        try:
            self.systray.shutdown()
        except Exception as e:
            return e


    def is_running(self):
        return self.systray is not None and self.execution_thread is not None


    def add_option(self, text, func):
        self.menu_options = self.menu_options + ((text, None, func),)

        # restart to update options
        if self.is_running():
            self.close()
            self.create()

    def set_hover_text(self, text):
        self.systray.update(hover_text=text)

    def set_icon(self, icon_path:str):
        self.systray.update(icon=icon_path)

    # systay callbacks
    def on_double_click(self, sys):
        print("double click!")

    def on_quit_callback(self, sys):
        print("systray is closed")
        self.systray = None
        self.execution_thread = None

    def on_open_league_of_legends(self, sys):
        print("abriendo lol")
        os.popen(Config.get("league_of_legends_path"))

