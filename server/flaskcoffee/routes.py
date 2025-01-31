from flask import request, jsonify, url_for, redirect, render_template, flash
from datetime import datetime
from flaskcoffee import app, db, bcrypt, coffee_advisor
from flaskcoffee.models import User, Post, CoffeeSetup


@app.route('/recommendation', methods=['POST'])
def recommendation_json():
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


@app.route('/register', methods=['GET', 'POST'])
def register_user_json():
    try:
        print(request)
        data = request.get_json()
        print("Received data:", data)
        username = data.get('username')
        print("Username:", username)
        email = data.get('email')
        print("Email:", email)
        password = data.get('password')
        print("Password:", password)
        confirm_password = data.get('confirm_password')
        print("Confirm Password:", confirm_password)

        if password != confirm_password:
            
            return flash('Passwords do not match', 'danger')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        #redirect(url_for('login'))
        return jsonify({
            "message": "registration successful"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['GET', 'POST'])
def login_user_json():
    try:
        print(request)
        data = request.get_json()
        print("Received data:", data)
        email = data.get('email')
        print("Email:", email)
        password = data.get('password')
        print("Password:", password)
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({
            "message": "login successful"
            }), 200
        else:
            return jsonify({
            "message": "User Login failed"
            }), 300
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/saveSetup', methods=['POST'])
def save_setup():
    try:
        print(request)
        data = request.get_json()
        print("Received data:", data)
        drink = data.get('drink')
        print("Drink:", drink)
        coffee_beans = data.get('coffeeBeans')
        print("Coffee Beans:", coffee_beans)
        brewing_device = data.get('brewingDevice')
        print("Brewing Device:", brewing_device)
        grinder = data.get('grinder')
        print("Grinder:", grinder)
        grind_setting = data.get('grindSetting')
        print("Grind Setting:", grind_setting)
        
        setup = CoffeeSetup(drink=drink, coffee_beans=coffee_beans, brewing_device=brewing_device, grinder=grinder, grind_setting=grind_setting)
        
        db.session.add(setup)
        db.session.commit()
        return jsonify({
            "message": "Setup saved successfully"
        }), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
