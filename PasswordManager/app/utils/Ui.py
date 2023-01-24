import ctypes
import winsound


def popUp(title: str, text: str):
    winsound.Beep(640, 500)
    ctypes.windll.user32.MessageBoxW(None, title, text, None)
