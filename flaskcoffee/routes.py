import os
from flask import request, jsonify, url_for, redirect, render_template, flash, make_response, send_from_directory, current_app
from flaskcoffee import app, db, bcrypt, coffee_advisor
from flaskcoffee.models import User, CoffeeSetup, CoffeeJourney, JourneyCard
from datetime import datetime, timedelta, timezone

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=2))
        if target_timestamp > exp_timestamp:
            print("Refreshing JWT")
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

@app.route('/verify-auth', methods=['GET'])
@jwt_required(optional=True)
def verify_auth():
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        
        # If we have a user ID, find user in database
        if user_id:
            user = User.query.get(int(user_id))
            if user:
                return jsonify({
                    "is_authenticated": True,
                    "user_id": user.id,
                    "username": user.username
                }), 200
        
        # If no user_id or no user found, return not authenticated
        return jsonify({
            "is_authenticated": False
        }), 200
        
    except Exception as e:
        print(f"Auth verification error: {str(e)}")
        return jsonify({
            "is_authenticated": False,
            "error": str(e)
        }), 500

@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Create a response that will clear the JWT cookie
        response = make_response(jsonify({"message": "Logged out successfully"}))
        unset_jwt_cookies(response)
        # response.set_cookie('access_token_cookie', '', expires=0)
        return response, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        
        return jsonify({
            "message": "registration successful"
        }), 200
    except Exception as e:
        db.session.rollback() # Rollback the session on error
        app.logger.exception("Error during user registration") # Logs the error with traceback
        
        return jsonify({"error": "An internal error occurred during registration."}), 500


@app.route('/login', methods=['POST'])
def login_user_json():
    # if request.method == 'GET':
    #     return render_template('login.html')
    if request.method == 'POST':
        try:
            print(request)
            data = request.get_json()
            print("Received data:", data)
            email = data.get('email')
            print("Email:", email)
            password = data.get('password')
            # print("Password:", password)
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token_value = create_access_token(identity=str(user.id))

                response = make_response(jsonify({
                    "login_success": True,
                    "user_id": user.id,
                    "username": user.username
                }))

                set_access_cookies(response, access_token_value)

                print(f"Login successful for user {user.username}. Response data: {response.get_json()}")

                return response
            else:
                return jsonify({
                    "message": "User Login failed",
                    "login_success": False
                }), 401
        except Exception as e:
            # It's good practice to log the error too
            app.logger.exception("Error during login attempt")
            return jsonify({"error": str(e)}), 500
    
@app.route('/saveSetup', methods=['POST'])
@jwt_required(optional=True)  # Makes JWT optional but still verifies it if present
def save_setup():
    try:
        user_id = None
        user = None
        
        try:
            user_id = get_jwt_identity()
            if user_id:
                # Convert string user_id to integer before query
                user_id = int(user_id)
                print(f"User ID from JWT: {user_id}")
                user = User.query.get(user_id)
                if user:
                    print(f"Found user: {user.username}")
                else:
                    print(f"No user found with ID: {user_id}")
        except Exception as jwt_error:
            print(f"JWT error: {str(jwt_error)}")
            user = None
            
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
       
        
        setup = CoffeeSetup(drink=drink, coffee_beans=coffee_beans, brewing_device=brewing_device, grinder=grinder, grind_setting=grind_setting, user_id=user.id if user else None)
        
        db.session.add(setup)
        db.session.commit()
        return jsonify({
            "message": "Setup saved successfully"
        }), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    

@app.route('/getSetup', methods=['GET'])
@jwt_required(optional=True)
def get_setup():
    try:
        # Get user ID if present in JWT token
        user_id = None
        user = None
        
        try:
            user_id = get_jwt_identity()
            if user_id:
                # Convert string user_id to integer before query
                user_id = int(user_id)
                print(f"User ID from JWT: {user_id}")
                user = User.query.get(user_id)
                if user:
                    print(f"Found user: {user.username}")
                else:
                    print(f"No user found with ID: {user_id}")
            else:
                print("No user_id found in JWT")
        except Exception as jwt_error:
            print(f"JWT error: {str(jwt_error)}")
        
        # Create base query
        query = CoffeeSetup.query.order_by(CoffeeSetup.id.desc())
        
        # Apply user filter if user_id is provided
        if user:
            print(f"Filtering setups for user: {user.username}")
            query = query.filter_by(user_id=user.id)
        else:
            print("Not filtering by user")
            
        # Get limited results
        setups = query.limit(4).all()
        
        setup_list = []
        for setup in setups:
            setup_list.append({
                "id": setup.id,
                "drink": setup.drink,
                "coffeeBeans": setup.coffee_beans,
                "brewingDevice": setup.brewing_device,
                "grinder": setup.grinder,
                "grindSetting": setup.grind_setting,
                "user_id": setup.user_id
            })
        
        print(f"Returning {len(setup_list)} setups")
        return jsonify({
            "setups": setup_list
        }), 200
    except Exception as e:
        print(f"Error in getSetup: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/archiveSetup', methods=['POST', 'GET'])
@jwt_required(optional=True)
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

            # First try to get user from JWT token (more secure)
            user_id = None
            user = None
            
            try:
                user_id = get_jwt_identity()
                if user_id:
                    user_id = int(user_id)
                    user = User.query.get(user_id)  # Correct syntax - no keyword args
                    print(f"User from JWT: {user.username if user else None}")
            except Exception as jwt_error:
                print(f"JWT error: {str(jwt_error)}")
            
            # Only fall back to request data if no JWT user (less secure)
            if not user:
                user_id_from_request = data.get('user_id')
                if user_id_from_request:
                    user = User.query.get(user_id_from_request)  # Correct syntax
                    print(f"User from request: {user.username if user else None}")

            # Create journey with user ID if available
            journey = CoffeeJourney(
                drink=drink, 
                coffee_beans=coffee_beans, 
                brewing_device=brewing_device, 
                grinder=grinder, 
                grind_setting=grind_setting, 
                iteration=1, 
                user_id=user.id if user else None
            )
            

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
                "message": "Journey archived successfully",
                "journey_id": journey.id
            }), 200
        except Exception as e:
            print("Error:", str(e))
            db.session.rollback()  # Add rollback to prevent partial commits on error
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':
        try:
            # First try to get user from JWT token
            user_id = None
            user = None
            
            try:
                user_id = get_jwt_identity()
                if user_id:
                    # Convert string user_id to integer before query
                    user_id = int(user_id)
                    print(f"User ID from JWT: {user_id}")
                    user = User.query.get(user_id)
                    print(f"User from JWT: {user.username if user else None}")
            except Exception as jwt_error:
                print(f"JWT error: {str(jwt_error)}")
            
            # If no JWT user, fall back to query param
            if user_id is None:
                user_id = int(user_id)
                user_id = request.args.get('user_id')
                print(f"User ID from query param: {user_id}")
            
            # Create base query
            query = CoffeeJourney.query.order_by(CoffeeJourney.id.desc())
            
            # Apply user filter if user_id is provided
            if user:
                query = query.filter_by(user_id=user.id)
                print(f"Filtering journeys by user_id: {user_id}")
                

            journeys = query.limit(10).all()
            # journeys = CoffeeJourney.query.order_by(CoffeeJourney.id.desc()).limit(10).all()
            
            journey_list = []
            for journey in journeys:
                journey_list.append({
                    "id": journey.id,
                    "drink": journey.drink,
                    "coffeeBeans": journey.coffee_beans,
                    "brewingDevice": journey.brewing_device,
                    "grinder": journey.grinder,
                    "grindSetting": journey.grind_setting,
                    "iteration": journey.iteration,
                    "user_id": journey.user_id
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
    
    @app.route("/protected")
    @jwt_required()
    def protected():
        return jsonify(foo="bar")

@app.route('/debug-serve')
def debug_serve_frontend():
    static_folder_path = app.static_folder
    index_path = os.path.join(static_folder_path, 'index.html')
    index_exists = os.path.exists(index_path)
    return f"""
    <h1>Debug Information</h1>
    <p>Requested Path: /debug-serve</p>
    <p>app.static_folder: {static_folder_path}</p>
    <p>Checking for index.html at: {index_path}</p>
    <p>Does index.html exist at that path? {index_exists}</p>
    """


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    # --- Add Logging ---
    app.logger.debug(f"serve_frontend called with path: {path}")
    app.logger.debug(f"app.static_folder is: {app.static_folder}")
    # -------------------

    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
         # --- Add Logging ---
        asset_path = os.path.join(app.static_folder, path)
        app.logger.debug(f"Attempting to serve specific asset: {asset_path}")
        # -------------------
        return send_from_directory(app.static_folder, path)
    else:
        # --- Add Logging ---
        index_path = os.path.join(app.static_folder, 'index.html')
        app.logger.debug(f"Attempting to serve index.html from path: {index_path}")
        exists = os.path.exists(index_path)
        app.logger.debug(f"os.path.exists({index_path}) returned: {exists}")
        # -------------------
        if exists:
            return send_from_directory(app.static_folder, 'index.html')
        else:
            app.logger.error(f"Failed to find index.html at expected path: {index_path}") 
            return "Frontend index.html not found.", 404