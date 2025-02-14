from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    in_diet = db.Column(db.String(3), nullable=False)  # "sim" ou "não"

