#Библиотеки и заголовочные файлы, используемые для этого файла
from datetime import timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from app import db
from models import User
from utils import hash_password, check_password_hash

#Создание группы маршрутов с префиксом /api/auth
bp = Blueprint("auth", __name__, url_prefix="/api/auth")

#Рекурсия, вызываемая в случае неверного ввода данных
def _bad_request(msg="Bad request", code=400):
    return jsonify({"msg": msg}), code

#Маршрут регистрации, при успешной регистрации вернёт временный токен, токен продления первого и информацию пользователя
@bp.route("/register", methods=["POST"])
def register():
    #Создание переменных, в которых будут токены, а также почта, пароль и имя пользователя
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    display_name = data.get("display_name")
    #Проверка на неправильный ввод почты и пароля
    if not email or not password:
        return _bad_request("email and password are required", 400)
    #Проверка на длину почты
    if len(password) < 6:
        return _bad_request("password must be at least 6 characters", 400)
    # Проверка на занятость почты
    if User.query.filter_by(email=email).first():
        return _bad_request("email already registered", 400)
    # Создание пользователя
    pw_hash = hash_password(password)
    user = User(email=email, password_hash=pw_hash, display_name=display_name)
    db.session.add(user)
    db.session.commit()
    # Создание токенов
    access_expires = timedelta(seconds=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 60 * 60 * 12))
    access_token = create_access_token(identity=user.id, expires_delta=access_expires)
    refresh_token = create_refresh_token(identity=user.id)
    #Если всё нормально, то вернёт токены и информацию и выйдет с кодом успеха 201
    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"id": user.id, "email": user.email, "display_name": user.display_name},
            }
        ),
        201,
    )

#Маршрут входа, при успешной регистрации вернёт то, что и прошлый маршрут
@bp.route("/login", methods=["POST"])
def login():
    #Создание переменных, в которых будут токены, а также почта, пароль и имя пользователя
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    #Проверка на неправильный ввод почты и пароля
    if not email or not password:
        return _bad_request("email and password are required", 400)
    #Создание переменной пользователя + проверка на неверный пароль
    user = User.query.filter_by(email=email).first()
    if not user or not user.password_hash or not check_password_hash(user.password_hash, password):
        return _bad_request("invalid credentials", 401)
    #Создание токенов
    access_expires = timedelta(seconds=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 60 * 60 * 12))
    access_token = create_access_token(identity=user.id, expires_delta=access_expires)
    refresh_token = create_refresh_token(identity=user.id)
    #Если всё нормально, то вернёт токены и информацию и выйдет с кодом успеха 200
    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"id": user.id, "email": user.email, "display_name": user.display_name},
            }
        ),
        200,
    )

#Маршрут продления временного токена (с отдельным маршрутом jwt_required)
@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    #Создание переменной, которая продлевает токен
    identity = get_jwt_identity()
    #Продление токена
    access_expires = timedelta(seconds=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 60 * 60 * 12))
    access_token = create_access_token(identity=identity, expires_delta=access_expires)
    return jsonify({"access_token": access_token}), 200

#Маршрут просмотра информации о себе (тоже с отдельным маршрутом jwt_required)
@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    #Создание переменных, в которых будет храниться id и информация пользователя по id
    uid = get_jwt_identity()
    user = User.query.get(uid)
    #Проверка на существование пользователя(если есть пользователь, то выведет его id, почту и имя
    if not user:
        return _bad_request("user not found", 404)
    return jsonify({"id": user.id, "email": user.email, "display_name": user.display_name}), 200
