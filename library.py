from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.sqlite"
db = SQLAlchemy(app)


import routes.authors
import routes.users
import routes.books
import routes.loans

