from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha512', salt_length=16)
    
    # Returns true if the password is correct or false if it's incorrect
    def check_password(self, password):    
        return check_password_hash(self.password, password)

class Actuator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)
    state_current = db.Column(db.Boolean, nullable=False)
    ip = db.Column(db.String(15), index=True, nullable=False, unique=True)

    def __init__(self, name:str, ip=None):
        self.name = name
        self.state_current = False
        self.ip = ip

    def updateState(self, state:bool):
        self.state_current = state

    def __repr__(self):
        return '<Actuator {}>'.format(self.id, self.name, self.ip, self.state_current)

class ControllerLed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)
    # GPIO pin numbers for red, green, blue led wires
    gpio_red = db.Column(db.Integer, nullable=False)
    gpio_green = db.Column(db.Integer, nullable=False)
    gpio_blue = db.Column(db.Integer, nullable=False)
    # Led state
    state_current = db.Column(db.Boolean, nullable=False)
    state_colorshift = db.Column(db.Boolean, nullable=False)
    state_red = db.Column(db.Integer, nullable=False)
    state_green = db.Column(db.Integer, nullable=False)
    state_blue = db.Column(db.Integer, nullable=False)
    state_brightness = db.Column(db.Float, nullable=False)

    def __init__(self, name:str, gpio_red:int, gpio_green:int, gpio_blue:int):
        self.name = name
        
        self.gpio_red = gpio_red
        self.gpio_green = gpio_green
        self.gpio_blue = gpio_blue

        # Default values
        self.state_current = False
        self.state_colorshift = False
        self.state_red = 125
        self.state_green = 125
        self.state_blue = 125
        self.state_brightness = 25.5

    def updateCurrentState(self, state:bool):
        self.state_current = state

    def updateColor(self, red:int, green:int, blue:int):
        self.state_red = red
        self.state_green = green
        self.state_blue = blue
    
    def updateBrightness(self, brightness:float):
        self.state_brightness = brightness

    def updateColorshiftState(self, state:bool):
        self.state_colorshift = state

    def __repr__(self):
        return '<Led Controller {}>'.format(self.name, self.state_current, self.gpio_red, self.gpio_green, self.gpio_blue)

# Dictionary meant for assigning data_type string to an integer value, 
#   to be inserted in the database instead.
data_type_dict = {
    'dht11_temperature' : 0,
    'dht11_humidity' : 1
}

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now, nullable=False)
    data_reading = db.Column(db.Float, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)

    def __init__(self, timestamp, data_reading, data_type):
        self.timestamp = timestamp
        self.data_reading = data_reading
        self.data_type = data_type
    
    def __repr__(self):
        return '<Reading {}>'.format(self.id, self.data_reading)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Time(), index=True, nullable=False)
    actuator_id = db.Column(db.Integer, db.ForeignKey('actuator.id'), nullable=False)    

    def __init__(self, timestamp:datetime.time, actuator_id:int):
        self.timestamp = timestamp
        self.actuator_id = actuator_id

    def __repr__(self):
        return '<Schedule {}>'.format(self.id, self.timestamp, self.actuator_id)