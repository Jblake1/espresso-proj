from flask import request, jsonify, url_for, redirect, render_template, flash
from datetime import datetime
from flaskcoffee import app, db, bcrypt, coffee_advisor
from flaskcoffee.models import User, Post


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
            "messsage": "User registered successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login_user_json():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

