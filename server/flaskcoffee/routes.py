from flask import request, jsonify, url_for, redirect, render_template, flash
from datetime import datetime
from flaskcoffee import app
from flaskcoffee import coffee_advisor
from flaskcoffee.models import User, Post

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
        coffee_beans = data.get('coffee_beans')
        
        # Check for missing fields
        if not all([brewing_device, drink, grinder, coffee_beans]):
            return jsonify({"error": "Missing one or more required fields: brewing_device, drink, grinder, coffee_beans"}), 400

        # Get coffee advice
        advice = coffee_advisor.get_coffee_advice(drink, coffee_beans, brewing_device, grinder)
        print("Advice:", advice)


        # Return the parsed values
        return jsonify({
            "advice":advice
        }), 200
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500
    
@app.route('/about')
def about():
    return"<h1> About Page </h1>"
