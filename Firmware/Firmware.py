"""
KMK Macropad Configuration - Complete Version
9-key macropad with rotary encoder and OLED display
"""

import board
import neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.modules.encoder import EncoderHandler
from kmk.handlers.sequences import simple_key_sequence, send_string

# Import OLED display extension
from oled_display import OLEDDisplay

# Initialize keyboard
keyboard = KMKKeyboard()

# Enable media keys extension
media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

# ==================== RGB LED CONFIGURATION ====================
# Configure RGB LEDs (WS2812/NeoPixel)
# Update these settings based on your LED setup:
LED_PIN = board.GP15  # Update this to your LED data pin
NUM_LEDS = 9  # Number of RGB LEDs (one per key)
LED_ORDER = neopixel.GRB  # Color order (GRB or RGB depending on your LEDs)

# Initialize RGB extension
rgb = RGB(
    pixel_pin=LED_PIN,
    num_pixels=NUM_LEDS,
    val_limit=100,  # Brightness limit (0-255, lower = dimmer)
    hue_default=0,  # Default hue (0-360)
    sat_default=100,  # Default saturation (0-100)
    val_default=50,  # Default brightness (0-100)
    animation_mode=AnimationModes.STATIC,  # Start with static color
)
keyboard.extensions.append(rgb)

# LED state tracking
class LEDController:
    def __init__(self, rgb_extension):
        self.rgb = rgb_extension
        self.is_on = False
        self.current_color_index = 0
        self.colors = [
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (255, 255, 0),    # Yellow
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 128, 0),    # Orange
            (128, 0, 255),    # Purple
            (255, 255, 255),  # White
        ]
    
    def toggle_leds(self):
        """Turn LEDs on/off"""
        if self.is_on:
            # Turn off
            self.rgb.set_rgb_fill(0, 0, 0)
            self.is_on = False
        else:
            # Turn on with current color
            color = self.colors[self.current_color_index]
            self.rgb.set_rgb_fill(*color)
            self.is_on = True
    
    def change_color(self):
        """Cycle to next color"""
        if self.is_on:
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            color = self.colors[self.current_color_index]
            self.rgb.set_rgb_fill(*color)
        else:
            # Turn on if off
            self.toggle_leds()

led_controller = LEDController(rgb)

# Initialize OLED display
# Adjust I2C pins based on your schematic (GP0=SDA, GP1=SCL are common)
oled = OLEDDisplay(scl_pin=board.GP1, sda_pin=board.GP0)
keyboard.extensions.append(oled)

# Configure matrix (3x3 grid based on schematic)
keyboard.col_pins = (board.GP2, board.GP3, board.GP4)
keyboard.row_pins = (board.GP5, board.GP6, board.GP7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary Encoder Configuration
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Rotary encoder pins - adjust based on your schematic
# Format: (Pin A, Pin B, Button Pin, is_inverted)
encoder_handler.pins = (
    (board.GP8, board.GP9, board.GP10, False),
)


# Custom volume encoder handler that updates display
class VolumeEncoder:
    def __init__(self, display):
        self.display = display
        
    def volume_up(self):
        self.display.volume_up(5)
        return KC.VOLU
        
    def volume_down(self):
        self.display.volume_down(5)
        return KC.VOLD

vol_encoder = VolumeEncoder(oled)

# Map encoder to volume control with display update
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD, KC.MUTE),),
]


# ==================== CUSTOM MACROS ====================

def screenshot_macro():
    """Take screenshot (Windows: Win+Shift+S)"""
    return simple_key_sequence([
        KC.LGUI(KC.LSFT(KC.S))
    ])

def open_spotify():
    """Open Spotify"""
    return simple_key_sequence([
        KC.LGUI,
        KC.MACRO_SLEEP_MS(100),
        send_string("spotify"),
        KC.MACRO_SLEEP_MS(200),
        KC.ENTER
    ])

def open_chrome():
    """Open Chrome"""
    return simple_key_sequence([
        KC.LGUI,
        KC.MACRO_SLEEP_MS(100),
        send_string("chrome"),
        KC.MACRO_SLEEP_MS(200),
        KC.ENTER
    ])

def new_tab():
    """Open new tab (Ctrl+T)"""
    return simple_key_sequence([
        KC.LCTL(KC.T)
    ])

def led_toggle():
    """Toggle LED on/off"""
    def _toggle():
        led_controller.toggle_leds()
    return _toggle

def led_color_change():
    """Change LED color"""
    def _change():
        led_controller.change_color()
    return _change

def shutdown_pc():
    """Shutdown PC (Windows: Win+X, U, U)"""
    return simple_key_sequence([
        KC.LGUI(KC.X),
        KC.MACRO_SLEEP_MS(300),
        KC.U,
        KC.MACRO_SLEEP_MS(100),
        KC.U
    ])


# Register custom keys
KC.SCREENSHOT = screenshot_macro()
KC.SPOTIFY = open_spotify()
KC.CHROME = open_chrome()
KC.LED_TOGGLE = led_toggle()
KC.LED_COLOR = led_color_change()
KC.SHUTDOWN = shutdown_pc()


# ==================== KEYMAP LAYOUT ====================
# Button layout (3x3 grid):
# [1: Copy]      [2: Paste]      [3: Screenshot]
# [4: Pause]     [5: Spotify]    [6: Chrome]
# [7: LED On/Off] [8: LED Color] [9: Shutdown]
#
# Rotary Encoder: Volume Up/Down, Press to Mute

keyboard.keymap = [
    [
        KC.LCTL(KC.C),    # Button 1: Copy (Ctrl+C)
        KC.LCTL(KC.V),    # Button 2: Paste (Ctrl+V)
        KC.SCREENSHOT,    # Button 3: Screenshot (Win+Shift+S)
        
        KC.MPLY,          # Button 4: Play/Pause media
        KC.SPOTIFY,       # Button 5: Open Spotify
        KC.CHROME,        # Button 6: Open Chrome
        
        KC.LED_TOGGLE,    # Button 7: Toggle LED On/Off
        KC.LED_COLOR,     # Button 8: Change LED Color
        KC.SHUTDOWN,      # Button 9: Shutdown PC
    ]
]
