from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO, send, emit
import eventlet

# Monkey Patching
eventlet.monkey_patch()

# Flask App
app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, async_mode='eventlet')


# Database Related
# 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Signing Users Related
# 
login = LoginManager(app)
# Specify view that handles signing in
login.login_view = 'sign_in'

from app import routes, models, forms, errors, socketio_server

def hello(world:str):
    while True:
        print('hello ',world, sys.stdout)
        socketio.sleep(5)

if __name__ == "__main__":
    socketio.run(app)
    socketio.start_background_task(target=hello)#, args=('world'))
