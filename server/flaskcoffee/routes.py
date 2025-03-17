from flask import request, jsonify, url_for, redirect, render_template, flash
from datetime import datetime
from flaskcoffee import app, db, bcrypt, coffee_advisor
from flaskcoffee.models import User, CoffeeSetup, CoffeeJourney, JourneyCard


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
    

@app.route('/getSetup', methods=['GET'])
def get_setup():
    try:
        setups = CoffeeSetup.query.order_by(CoffeeSetup.id.desc()).limit(4).all()
        setup_list = []
        for setup in setups:
            setup_list.append({
                "drink": setup.drink,
                "coffeeBeans": setup.coffee_beans,
                "brewingDevice": setup.brewing_device,
                "grinder": setup.grinder,
                "grindSetting": setup.grind_setting
            })
        return jsonify({
            "setups": setup_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/archiveSetup', methods=['POST', 'GET'])
def archive_setup():
    if request.method == 'POST':
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
            
            
            journey = CoffeeJourney(drink=drink, coffee_beans=coffee_beans, brewing_device=brewing_device, grinder=grinder, grind_setting=grind_setting, iteration=1)
            
            

            db.session.add(journey)
            db.session.flush()  # This assigns the ID to journey without committing
            
            # Now create the first journey card using the journey's ID and grind setting
            initial_card = JourneyCard(
                journey_id=journey.id,
                grind_setting=grind_setting,
                notes="(notes)",
                shot_time="(shot time)"
            )
            
            db.session.add(initial_card)
            db.session.commit()  # Commit both the journey and the card

            return jsonify({
                "message": "Journey archived successfully"
            }), 200
        except Exception as e:
            print("Error:", str(e))
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':
        try:
            journeys = CoffeeJourney.query.order_by(CoffeeJourney.id.desc()).limit(10).all()
            journey_list = []
            for journey in journeys:
                journey_list.append({
                    "id": journey.id,
                    "drink": journey.drink,
                    "coffeeBeans": journey.coffee_beans,
                    "brewingDevice": journey.brewing_device,
                    "grinder": journey.grinder,
                    "grindSetting": journey.grind_setting,
                    "iteration": journey.iteration
                })
            return jsonify({
                "journeys": journey_list
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Method not allowed"}), 405

@app.route('/journeyCard', methods=['POST', 'GET'])
def journey_card():
    if request.method == 'POST':
        try:
            print(request)
            data = request.get_json()
            print("Received data:", data)
            journey_id = data.get('journeyID')
            print("Journey ID:", journey_id)
            grind_setting = data.get('grindSetting', None)
            notes = data.get('notes', None)
            shot_time = data.get('shotTime', None)
            iteration = data.get('iteration', None)
           
            card = JourneyCard(journey_id=journey_id, grind_setting=grind_setting, iteration=iteration, notes=notes, shot_time=shot_time)
            
            db.session.add(card)
            db.session.commit()
            return jsonify({
                "message": "Card saved successfully"
            }), 200
        except Exception as e:
            print("Error:", str(e))
            return jsonify({"error": str(e)}), 500
        
    elif request.method == 'GET':
        try:
            journey_id = request.args.get('journeyID')
            print(f"Received journeyID: {journey_id}")
            cards = JourneyCard.query.filter_by(journey_id=journey_id).order_by(JourneyCard.id.desc()).limit(3).all()
            card_list = []
            for card in cards:
                card_list.append({
                    "id": card.id,
                    "grindSetting": card.grind_setting,
                    "iteration": card.iteration,
                    "notes": card.notes,
                    "journey_id": card.journey_id,
                    "datePosted": card.date_posted,
                    "shotTime": card.shot_time
                })
            return jsonify({
                "journeyCards": card_list
            }), 200
        except Exception as e:
            print("Error:", str(e))
            return jsonify({"error": str(e)}), 500
        
@app.route('/journeyCardEdit', methods=['POST'])
def journey_card_edit():
    try:
        print(request)
        data = request.get_json()
        print("Received data:", data)
        card_id = data.get('id')
        print("Card ID:", card_id)
        grind_setting = data.get('grindSetting')
        shot_time = data.get('shotTime')
        notes = data.get('notes')
        
        
        card = JourneyCard.query.get(card_id)
        card.grind_setting = grind_setting
        card.notes = notes
        card.shot_time = shot_time
        db.session.commit()

        return jsonify({
            "message": "Card updated successfully"
        }), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/journeyCardDelete', methods=['POST'])
def journey_card_delete():
    try:
        print(request)
        data = request.get_json()
        print("Received data:", data)
        card_id = data.get('id')
        print("Card ID:", card_id)
        
        card = JourneyCard.query.get(card_id)
        db.session.delete(card)
        db.session.commit()

        return jsonify({
            "message": "Card deleted successfully"
        }), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/journeyDelete', methods=['POST'])
def journey_delete():
    try:
        print(request)
        data = request.get_json()
        print("Received data:", data)
        journey_id = data.get('id')
        print("Journey ID:", journey_id)
        
        # First, delete all journey cards associated with this journey
        JourneyCard.query.filter_by(journey_id=journey_id).delete()
        
        # Then delete the journey itself
        journey = CoffeeJourney.query.get(journey_id)
        db.session.delete(journey)
        
        # Commit all changes at once
        db.session.commit()

        return jsonify({
            "message": "Journey and all associated cards deleted successfully"
        }), 200
    except Exception as e:
        print("Error:", str(e))
        # Roll back in case of error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500