"""
Seed script to create an admin user and a sample patient + booking.
Run with: python backend/seed.py
"""
from backend.app import create_app, db
from backend.models import User, Patient, Booking
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(phone='9999999999').first():
        admin = User(name='Admin', phone='9999999999', role='admin')
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.flush()

        user = User(name='Test Patient', phone='9876543210', role='patient')
        user.set_password('password')
        db.session.add(user)
        db.session.flush()

        patient = Patient(user_id=user.id, address='Delhi, India', medical_history='None')
        db.session.add(patient)
        db.session.flush()

        booking = Booking(patient_id=patient.id, service='physiotherapy', datetime=datetime.utcnow() + timedelta(days=1), notes='Initial visit')
        db.session.add(booking)

        db.session.commit()
        print('Seed data created.')
    else:
        print('Seed data already present.')
