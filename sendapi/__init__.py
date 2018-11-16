
from flask import Flask
app = Flask(__name__)

from .routes import user
from .routes import parcel


if __name__=="__main__":
    app.run(debug=True)