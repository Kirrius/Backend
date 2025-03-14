from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import routes
from database_info import db_name, db_host, db_password, db_username
from database import db
application = Flask(__name__)
bcrypt_ = Bcrypt(application)

application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
db.init_app(application)
@application.route('/')
@application.route('/home')
def home():
    return "main page"


@application.route("/set_script_params", methods=["POST"])
def create_script():
    data = request.get_json(force=True)
    response = routes.set_script_params(data)
    return response

@application.route("/delete_script", methods=["DELETE"])
def delete_script():
    data = request.get_json(force=True)
    script_id = data.get("script_id")
    password = data.get("password")
    response = routes.delete_script(script_id, password)
    return response

@application.route("/get_script_params", methods=["GET"])
def get_script_params():
    script_id = request.args.get("script_id")
    response = routes.get_script_params(script_id)
    return response

@application.route("/set_new_controller", methods=["GET"])
def set_new_controller():
    response = routes.set_new_controller()
    return response

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run()