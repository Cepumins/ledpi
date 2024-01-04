import board
import neopixel

NUM_PIXELS = 150  # Change this to the number of LEDs you have

pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, brightness=1.0, auto_write=True, pixel_order=neopixel.RGBW)

def clearLEDs():
    for i in range(NUM_PIXELS):
        pixels[i] = (0, 0, 0, 0)
    pixels.show()

clearLEDs()