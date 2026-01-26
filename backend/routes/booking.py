from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import Booking, Patient
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
@jwt_required()
def list_bookings():
    user_id = get_jwt_identity()
    # Find patient record for user
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify([]), 200
    bookings = Booking.query.filter_by(patient_id=patient.id).order_by(Booking.datetime.desc()).all()
    result = []
    for b in bookings:
        result.append({
            'id': b.id,
            'service': b.service,
            'datetime': b.datetime.isoformat(),
            'notes': b.notes,
            'clinician_id': b.clinician_id
        })
    return jsonify(result), 200

@bookings_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({'msg': 'patient profile not found'}), 400

    data = request.get_json() or {}
    service = data.get('service')
    datetime_str = data.get('datetime')
    notes = data.get('notes', '')

    if not service or not datetime_str:
        return jsonify({'msg': 'service and datetime are required'}), 400

    try:
        dt = datetime.fromisoformat(datetime_str)
    except Exception:
        return jsonify({'msg': 'invalid datetime format, use ISO8601 e.g. 2026-01-26T15:00:00'}), 400

    booking = Booking(patient_id=patient.id, service=service, datetime=dt, notes=notes)
    db.session.add(booking)
    db.session.commit()

    return jsonify({'msg': 'booking created', 'booking_id': booking.id}), 201
