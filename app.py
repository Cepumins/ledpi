from flask import Flask, render_template, jsonify, request, redirect, url_for
import neopixel
import board
import threading


app = Flask(__name__)

settings_data = {
    'num_lights': 100,
    'width_lights': 10,
    'breathing_speed': 5,
    'wave_speed': 5
}

led_states = ["off"] * settings_data['num_lights']  # Assuming 100 LEDs

# LED Configuration
LED_PIN = board.D18  # GPIO 18
LED_COUNT = settings_data['num_lights']  # Number of LEDs
LED_BRIGHTNESS = 0.1  # Adjust as needed
LED_ORDER = neopixel.GRBW  # Adjust as needed for your LED strip type
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, pixel_order=LED_ORDER)

@app.route('/')
def index():
    return render_template('index.html', led_states=led_states, settings=settings_data)

@app.route('/settings')
def settings():
    return render_template('settings.html', settings=settings_data)

@app.route('/update_settings', methods=['POST'])
def update_settings():
    global led_states, settings_data
    # Update the settings data with the form values
    settings_data['num_lights'] = request.form.get('num_lights', type=int, default=settings_data['num_lights'])
    settings_data['width_lights'] = request.form.get('width_lights', type=int, default=settings_data['width_lights'])
    settings_data['breathing_speed'] = request.form.get('breathing_speed', type=float, default=settings_data['breathing_speed'])
    settings_data['wave_speed'] = request.form.get('wave_speed', type=float, default=settings_data['wave_speed'])

    num_lights = settings_data['num_lights']

    # Update led_states to reflect new number of lights
    if num_lights > len(led_states):
        # If the number of lights has increased, add more 'off' states
        led_states += ["off"] * (num_lights - len(led_states))
    else:
        # If the number has decreased, trim the led_states list
        led_states = led_states[:num_lights]

    # Redirect to the index page where the settings will be displayed
    return redirect(url_for('settings'))

@app.route('/get-led-status', methods=['GET'])
def get_led_status():
    return jsonify(led_states)

@app.route('/apply-color', methods=['POST'])
def apply_color():
    data = request.get_json()
    selected_leds = data.get('leds')
    hex_color = data.get('color')
    rgbw_color = hex_to_rgbw(hex_color)
    for led in selected_leds:
        led_id = int(led)
        led_states[led_id] = {"status": "on", "color": hex_color}
        pixels[led_id] = rgbw_color
    pixels.show()
        #current_state = led_states[led_id]
        #print(f"Previous status of led {led_id} is: {current_state['status']}")
        # Add logic to physically set LED color here
    print(f"Applied color {hex_color} to LEDs: {selected_leds}")
    return jsonify({"status": "success", "message": f"Color {hex_color} applied to LEDs: {selected_leds}"})

@app.route('/apply-effect', methods=['POST'])
def apply_effect():
    data = request.get_json()
    selected_leds = data.get('leds')
    effect = data.get('effect')
    for led in selected_leds:
        led_id = int(led)
        current_state = led_states[led_id]
        #print(f"Previous status of led {led_id} is: {current_state['status']}")
        if not isinstance(current_state, dict):
            current_state = {'status': 'unknown', 'color': '#FFFFFF'}
        # effects 
        if effect == 'off':
            led_states[led_id] = {'status': 'off', 'color': '#000000'}
            pixels[int(led_id)] = (0, 0, 0, 0)
        else:
            
            if effect == 'breathing':
                if current_state['status'] == 'off' or current_state['status'] == 'breathing':
                    pass
                else:
                    # Save the current color for the breathing effect
                    current_color = led_states[led_id]['color'] if led_states[led_id]['status'] != 'off' else '#FFFFFF'
                    led_states[led_id] = {'status': 'breathing', 'color': current_color}
            elif effect == 'wave':
                led_states[led_id] = {'status': 'wave', 'color': '#FFFFFF'}  # Default color for wave effect
    # Add logic to physically apply the effect to the LED here
    pixels.show()
    print(f"Applied {effect} effect to LEDs: {selected_leds}")
    return jsonify({"status": "success", "message": f"Applied {effect} to LEDs: {selected_leds}"})

@app.route('/apply-brightness', methods=['POST'])
def apply_brightness():
    data = request.get_json()
    selected_leds = data.get('leds', [])
    brightness_pct = data.get('bright', 100)  # Default to 100% if not provided

    def adjust_color_brightness(color, brightness_pct):
        if not color.startswith('#') or len(color) != 7:
            return color  # or some default like "#FFFFFF"

        # Parse the RGB components from the color
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

        # Calculate the maximum possible multiplier for each color
        r_mult = (256 / (r + 1)) * (brightness_pct / 100)
        g_mult = (256 / (g + 1)) * (brightness_pct / 100)
        b_mult = (256 / (b + 1)) * (brightness_pct / 100)

        # Find the smallest multiplier to preserve color ratios
        min_mult = min(r_mult, g_mult, b_mult)

        # Apply the multiplier and ensure no value exceeds 255
        r = min(int((r + 1) * min_mult), 255)
        g = min(int((g + 1) * min_mult), 255)
        b = min(int((b + 1) * min_mult), 255)

        # Return the adjusted color in hex format
        return f"#{r:02x}{g:02x}{b:02x}"

    for led in selected_leds:
        led_id = int(led)
        current_state = led_states[led_id]
        if current_state['status'] != 'off':
            current_color = current_state['color']
            new_color = adjust_color_brightness(current_color, brightness_pct)
            led_states[led_id] = {"status": "on", "color": new_color}
            rgbw_color = hex_to_rgbw(new_color)
            pixels[led_id] = rgbw_color
            #print(f"{led_id} new color: {new_color}")
        # Add logic to physically apply the brightness to the LED here
    pixels.show()
    print(f"Applied brightness {brightness_pct}% to LEDs: {selected_leds}")
    return jsonify({"status": "success", "message": f"Applied brightness to LEDs: {selected_leds}"})

def hex_to_rgbw(hex_color):
    # Strip the '#' character and convert the string to an integer
    hex_color = hex_color.lstrip('#')
    # Convert the string into three integers as a tuple (RGB)
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Calculate the white component as the minimum value of R, G, and B
    w = min(rgb)
    # Subtract the white component from each R, G, and B to get the new R, G, and B values
    rgbw = tuple(c - w for c in rgb) + (w,)
    
    return rgbw

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8778)