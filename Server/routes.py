from flask import jsonify, request
from database import db
from main import bcrypt_, db
from models import Script, Controller
import secrets

def set_script_params(data):
    existing_script = Script.query.filter_by(cloud_user_id=data.get("cloud_user_id")).first()

    if existing_script:
        existing_script.password = data.get("password")
        existing_script.min_moisture_soil = data.get("min_moisture_soil")
        existing_script.max_moisture_soil = data.get("max_moisture_soil")
        existing_script.min_humidity_air = data.get("min_humidity_air")
        existing_script.max_humidity_air = data.get("max_humidity_air")
        existing_script.min_temperature_air = data.get("min_temperature_air")
        existing_script.max_temperature_air = data.get("max_temperature_air")
        db.session.commit()
        return jsonify({"message": "Script params updated successfully", "script_id": existing_script.id}), 200
    else:
        new_script = Script(
            cloud_user_id=data.get("cloud_user_id"),
            password=data.get("password"),
            min_moisture_soil=data.get("min_moisture_soil"),
            max_moisture_soil=data.get("max_moisture_soil"),
            min_humidity_air=data.get("min_humidity_air"),
            max_humidity_air=data.get("max_humidity_air"),
            min_temperature_air=data.get("min_temperature_air"),
            max_temperature_air=data.get("max_temperature_air")
        )
        db.session.add(new_script)
        db.session.commit()
        return jsonify({"message": "Script added successfully", "script_id": new_script.id}), 200


def delete_script(script_id, password):
    existing_script = Script.query.filter_by(id=script_id).first()
    if existing_script:
        if bcrypt_.check_password_hash(existing_script.password, password):
            db.session.delete(existing_script)
            db.session.commit()
            return jsonify({"message": "Script deleted successfully"}), 200
        else:
            return jsonify({"message": "Incorrect password"}), 401
    else:
        return jsonify({"message": "No scripts found forr this user"}), 404


def get_script_params(script_id):
    script = Script.query.filter_by(id=script_id).first()

    if script:
        res = {
            "id": script.id,
            "cloud_user_id": script.cloud_user_id,
            "min_moisture_soil": script.min_moisture_soil,
            "max_moisture_soil": script.max_moisture_soil,
            "min_humidity_air": script.min_humidity_air,
            "max_humidity_air": script.max_humidity_air,
            "min_temperature_air": script.min_temperature_air,
            "max_temperature_air": script.max_temperature_air
        }
        return jsonify(res), 200
    else:
        return jsonify({"message": "Script with given id not found"}), 404

def set_new_controller():
    new_controller = Controller(password=secrets.token_hex(16))
    db.session.add(new_controller)
    db.session.commit()
    return jsonify({"id": new_controller.getId(), "password": new_controller.getPass()}), 200