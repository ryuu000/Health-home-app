from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import User, Patient
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')
    address = data.get('address', '')
    if not phone or not password:
        return jsonify({'msg': 'phone and password required'}), 400

    existing = User.query.filter_by(phone=phone).first()
    if existing:
        return jsonify({'msg': 'user already exists'}), 400

    user = User(name=name, phone=phone)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # get user.id

    patient = Patient(user_id=user.id, address=address)
    db.session.add(patient)
    db.session.commit()

    return jsonify({'msg': 'registered', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    phone = data.get('phone')
    password = data.get('password')
    if not phone or not password:
        return jsonify({'msg': 'phone and password required'}), 400

    user = User.query.filter_by(phone=phone).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=8))
    return jsonify({'access_token': access_token, 'user': {'id': user.id, 'phone': user.phone, 'name': user.name}}), 200
