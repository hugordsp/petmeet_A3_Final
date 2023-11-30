from flask import Flask
from users_routes import register_users_routes
from database_setup import *

app = Flask(__name__)

#register_pet_routes(app)
register_users_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
