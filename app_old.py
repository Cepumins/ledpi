from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize a list to track the mode of each LED
led_states = ["off"] * 100  # Assuming 100 LEDs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/turn-off-lights', methods=['POST'])
def turn_off_lights():
    global led_states
    led_states = ["off"] * 100  # Turn off all LEDs
    # Add logic to physically turn off the lights
    print("Lights turned off")
    return jsonify({"status": "success", "message": "Lights turned off"})

@app.route('/apply-effect', methods=['POST'])
def apply_effect():
    global led_states
    effect = request.args.get('effect')
    selected_leds = request.args.getlist('selected_leds')  # List of selected LEDs
    for led in selected_leds:
        led_states[int(led)] = effect  # Update the state of each selected LED

    # Call appropriate function based on effect
    if effect == 'wave':
        apply_wave_effect(selected_leds)
    elif effect == 'breathing':
        apply_breathing_effect(selected_leds)
    elif effect == 'static':
        apply_static_effect(selected_leds)
    # Add more effects as needed

    return jsonify({"status": "success", "message": f"{effect} effect applied"})

def apply_wave_effect(selected_leds):
    # Add logic for wave effect
    print("Applying wave effect to LEDs:", selected_leds)

def apply_breathing_effect(selected_leds):
    # Add logic for breathing effect
    print("Applying breathing effect to LEDs:", selected_leds)

def apply_static_effect(selected_leds):
    # Add logic for static effect
    print("Applying static effect to LEDs:", selected_leds)

# More effect functions as needed

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8778)
