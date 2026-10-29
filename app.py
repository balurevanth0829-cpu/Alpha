from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_temperature_status(celsius):
    if celsius < -20:
        return "Extremely Cold", "Dangerously cold. Risk of frostbite."
    elif celsius < 0:
        return "Very Cold", "Freezing temperatures. Make sure to bundle up!"
    elif celsius < 10:
        return "Cold", "It's chilly outside. A warm jacket is recommended."
    elif celsius < 20:
        return "Cool", "A mild and cool temperature. A light sweater is perfect."
    elif celsius <= 28:
        return "Comfortable", f"{round(celsius)}°C is generally considered a very comfortable room temperature."
    elif celsius < 35:
        return "Warm", "It's getting warm. Stay hydrated and wear light clothing."
    elif celsius < 40:
        return "Hot", "Hot weather! Avoid prolonged sun exposure during peak hours."
    else:
        return "Extremely Hot", "Dangerously hot. Seek shade, stay indoors with AC, and drink plenty of water."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    try:
        temp_str = data.get('temperature', '').strip()
        if not temp_str:
            return jsonify({"error": "Please enter a temperature value."}), 400
        temp = float(temp_str)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid temperature value. Please enter a valid number."}), 400
        
    unit = data.get('unit')
    
    if unit == 'C':
        c = temp
        f = (c * 9/5) + 32
        k = c + 273.15
    elif unit == 'F':
        f = temp
        c = (f - 32) * 5/9
        k = c + 273.15
    elif unit == 'K':
        if temp < 0:
            return jsonify({"error": "Physically invalid. Temperature cannot be below Absolute Zero (0 K)."}), 400
        k = temp
        c = k - 273.15
        f = (c * 9/5) + 32
    else:
        return jsonify({"error": "Invalid unit selected."}), 400

    if k < 0:
        # Floating point precision might make k very slightly negative, let's round
        k = round(k, 10)
        if k < 0:
            return jsonify({"error": "Temperature is below Absolute Zero (0 K) which is physically impossible."}), 400
        
    status, insight = get_temperature_status(c)
    
    return jsonify({
        "C": round(c, 2),
        "F": round(f, 2),
        "K": round(k, 2),
        "status": status,
        "insight": insight,
        "raw_c": c # To help frontend with thermometer
    })

# Required for Vercel Serverless Functions
def handler(request, context):
    pass 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
