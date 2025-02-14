from flask import Flask
from database import db
from routes.meals import meals_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

app.register_blueprint(meals_bp)

if __name__ == "__main__":
    app.run(debug=True)
