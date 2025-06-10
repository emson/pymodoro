# src/pymodoro/keyboard.py
from pynput import keyboard

class KeyboardListener:
    def __init__(self, on_press_callback):
        self.on_press_callback = on_press_callback
        self.listener = keyboard.Listener(on_press=self._on_press)

    def _on_press(self, key):
        try:
            # Handle regular character keys
            char = key.char
        except AttributeError:
            # Handle special keys
            if key == keyboard.Key.space:
                char = ' '
            elif hasattr(key, 'char'):  # Handle KeyCode instances
                char = key.char
            else:
                return

        self.on_press_callback(char)
    
    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
