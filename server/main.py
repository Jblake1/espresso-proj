from flask import Flask, request, jsonify
from flask_cors import CORS
import coffee_advisor
import warnings

warnings.simplefilter("ignore")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/recommendation', methods=['POST'])
def parse_json():
    try:
        print(request)
        # Get JSON data from the request
        data = request.get_json()
        print("Received data:", data)
        # Extract the required values
        brewing_device = data.get('brewing_device')
        drink = data.get('drink')
        grinder = data.get('grinder')
        grind_range = data.get('grind_range')
        coffee_beans = data.get('coffee_beans')
        
        # Check for missing fields
        if not all([brewing_device, drink, grinder, coffee_beans, grind_range]):
            return jsonify({"error": "Missing one or more required fields: brewing_device, drink, grinder, coffee_beans, grind_range"}), 400

        # Get coffee advice
        advice = coffee_advisor.get_coffee_advice(drink, coffee_beans, brewing_device, grinder, grind_range)
        print("Advice:", advice)

        # Return the parsed values
        return jsonify({
            "advice":advice
        }), 200
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=4000)
