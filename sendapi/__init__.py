from flask import Flask
from config import app_config
from flask_jwt_extended import JWTManager
app = Flask(__name__)
app.config['JWT_SECRET_KEY']='secretkey'
jwt=JWTManager(app)
from .routes import user
from .routes import parcel
from .routes import auth



# if __name__=="__main__":
app.run(debug=True)