from datetime import datetime, timezone
from flaskcoffee import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    coffee_setups = db.relationship('CoffeeSetup', backref='user', lazy=True)
    coffee_journeys = db.relationship('CoffeeJourney', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class CoffeeSetup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink = db.Column(db.String(100), nullable=False)
    coffee_beans = db.Column(db.String(100), nullable=False)
    brewing_device = db.Column(db.String(100), nullable=False)
    grinder = db.Column(db.String(100), nullable=False)
    grind_setting = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    
    def __repr__(self):
        return f"CoffeeSetup('{self.drink}', '{self.brewing_device}', '{self.coffee_beans}', '{self.grinder}', '{self.grind_setting}')"
    
class CoffeeJourney(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink = db.Column(db.String(100), nullable=False)
    coffee_beans = db.Column(db.String(100), nullable=False)
    brewing_device = db.Column(db.String(100), nullable=False)
    grinder = db.Column(db.String(100), nullable=False)
    grind_setting = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    iteration = db.Column(db.Integer, nullable=False)
    cards = db.relationship('JourneyCard', backref='journey', lazy=True)

    def __repr__(self):
        return f"CoffeeJourney('{self.id}', '{self.drink}', '{self.brewing_device}', '{self.coffee_beans}', '{self.grinder}', '{self.grind_setting}', '{self.iteration}')"
    
class JourneyCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grind_setting = db.Column(db.String(100), nullable=False, default='(grind setting)')
    iteration = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    journey_id = db.Column(db.Integer, db.ForeignKey('coffee_journey.id'), nullable=False)
    shot_time = db.Column(db.String(20), nullable=True, default='(shot time)')
    notes = db.Column(db.Text, nullable=True, default='(notes)')

    def __init__(self, **kwargs):
        # Remove iteration if it's provided so we can calculate it
        if 'iteration' in kwargs:
            del kwargs['iteration']
            
        # Initialize all other attributes
        super(JourneyCard, self).__init__(**kwargs)
        
        # Calculate the iteration based on the highest iteration number + 1
        if hasattr(self, 'journey_id') and self.journey_id is not None:
            # Find the highest iteration number for this journey
            highest_card = JourneyCard.query.filter_by(journey_id=self.journey_id).order_by(JourneyCard.iteration.desc()).first()
            if highest_card:
                self.iteration = highest_card.iteration + 1
            else:
                self.iteration = 1
    
    def __repr__(self):
        return f"JourneyCard('{self.grind_setting}', '{self.iteration}', '{self.date_posted}', '{self.notes}', '{self.shot_time}', '{self.journey_id}')"