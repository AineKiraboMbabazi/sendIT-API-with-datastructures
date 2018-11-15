
from flask import Flask
app = Flask(__name__)

from .routes import user_routes
from .routes import parcel_routes


# if __name__=="__main__":
app.run(debug=True)