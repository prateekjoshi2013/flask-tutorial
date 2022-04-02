from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from http import HTTPStatus
from src.database import User,db
import validators

auth=Blueprint('auth',__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    if len(password)<6:
        return jsonify({'error':'Invalid password'}),HTTPStatus.BAD_REQUEST.value
    if len(username)<3 or not username.isalnum() or " " in username:
        return jsonify({'error':'Invalid username'}),HTTPStatus.BAD_REQUEST.value
    if not validators.email(email):
        return jsonify({'error':'Invalid email'}),HTTPStatus.BAD_REQUEST.value
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'Email is taken'}),HTTPStatus.CONFLICT.value
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':'Username is taken'}),HTTPStatus.CONFLICT.value

    pwd_hash=generate_password_hash(password)
    user=User(username=username,password=pwd_hash,email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message":"User created",
        "user":{
            "username":username,
            "email":email,
        }
    }),HTTPStatus.CREATED.value


@auth.get("/me")
def me():
    return {'user':'me'}