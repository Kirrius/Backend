from database import db

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cloud_user_id = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    min_moisture_soil = db.Column(db.Integer, nullable=False)
    max_moisture_soil = db.Column(db.Integer, nullable=False)
    min_humidity_air = db.Column(db.Integer, nullable=False)
    max_humidity_air = db.Column(db.Integer, nullable=False)
    min_temperature_air = db.Column(db.Integer, nullable=False)
    max_temperature_air = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Script {self.id}>"


class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)