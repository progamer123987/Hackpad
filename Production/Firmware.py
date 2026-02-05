Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import board

# KMK imports
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Macros

# ---- Main keyboard instance ----
keyboard = KMKKeyboard()

# ---- Modules ----
# Add encoders
... encoder_handler = EncoderHandler()
... keyboard.modules.append(encoder_handler)
... 
... # Add macros
... macros = Macros()
... keyboard.modules.append(macros)
... 
... # ---- Pins ----
... PINS = [board.D3, board.D4, board.D2, board.D1]
... 
... # ---- Key scanner (no matrix) ----
... keyboard.matrix = KeysScanner(
...     pins=PINS,
...     value_when_pressed=False,
... )
... 
... # ---- Rotary encoders ----
... encoder_handler.pins = (
...     (board.A0, board.A1),  # Encoder 1 - Volume
...     (board.A2, board.A3),  # Encoder 2 - Brightness
... )
... 
... encoder_handler.map = [
...     (KC.VOLD, KC.VOLU),       # Encoder 1
...     (KC.BR_DOWN, KC.BR_UP),   # Encoder 2
... ]
... 
... # ---- Keymap (1 layer) ----
... keyboard.keymap = [
...     [
...         KC.DELETE,                   # Button 1
...         KC.MACRO("Ctrl+Shift+T"),    # Button 2: Ctrl+Shift+T
...         KC.SCREENSHOT,               # Button 3
...         KC.LSHIFT,                   # Button 4 (hold = Shift)
...     ]
... ]
... 
... # ---- Start KMK ----
... if __name__ == '__main__':
