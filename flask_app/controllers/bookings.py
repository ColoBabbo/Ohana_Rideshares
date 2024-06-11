from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models import booking


@app.post('/add_booking')
def add_booking():
    if booking.Booking.is_legit_booking(request.form):
        new_booking = booking.Booking.insert_one(request.form)
    return redirect(url_for('show_all_requests'))

@app.get('/booking/<int:booking_id>/delete')
def delete_booking(booking_id:int):
    if session.get('logged_in'):
        booking.Booking.delete_one(booking_id)
        return redirect(url_for('show_all_requests'))
    return redirect(url_for('show_all_bookings'))