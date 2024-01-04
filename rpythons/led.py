import time
import board
import neopixel

# Configuration
LED_COUNT = 150  # Number of LEDs in your strip. Adjust this value.
LED_PIN = board.D18  # GPIO 18
LED_ORDER = neopixel.GRBW  # For SK6812 RGBW LEDs
LED_BRIGHTNESS = 0.1  # 10% brightness
LED_INVERT = False

pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, pixel_order=LED_ORDER, auto_write=False)

def colorWipe(color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(LED_COUNT):
        pixels[i] = color
        pixels.show()
        time.sleep(wait_ms/1000.0)

try:
    while True:
        # Red wipe
        colorWipe((255, 0, 0, 0))
        # Green wipe
        colorWipe((0, 255, 0, 0))
        # Blue wipe
        colorWipe((0, 0, 255, 0))
        # White wipe
        colorWipe((0, 0, 0, 255))
except KeyboardInterrupt:
    colorWipe((0, 0, 0, 0))  # Turn off all LEDs when Ctrl+C is pressed
