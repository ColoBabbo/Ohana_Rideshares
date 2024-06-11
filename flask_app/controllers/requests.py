from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models import request as ride_request
from flask_app.models import booking

@app.get('/dashboard')
def show_all_requests():
    if session.get('logged_in'):
        all_requests = ride_request.Request.get_all_with_booking()
        all_bookings = booking.Booking.get_all_with_driver()
        return render_template('show_all_requests.html', all_requests = all_requests, all_bookings = all_bookings)
    return redirect('/')

@app.get('/request/<int:request_id>')
def show_one_request(request_id:int):
    if session.get('logged_in'):
        this_request = ride_request.Request.get_one_with_booking(request_id)
        return render_template('show_one_request.html', this_request = this_request)
    return redirect('/')

@app.route('/add_request', methods=["GET", "POST"])
def add_request() -> None:
    if session.get('logged_in'):
        if request.method == "GET":
            if session.get('request_attempt'):
                pre_fill = {
                    'destination': session['request_attempt']['destination'],
                    'pickup': session['request_attempt']['pickup'],
                    'details': session['request_attempt']['details'],
                    'date': session['request_attempt']['date'],
                }
            else:
                pre_fill = {
                    'destination': '',
                    'pickup': '',
                    'details': '',
                    'date': '',
                }
            return render_template('new_request.html', pre_fill = pre_fill)
        elif request.method == "POST":
            if ride_request.Request.is_legit_request(request.form):
                new_request = ride_request.Request.insert_one(request.form)
                if session.get('request_attempt'):
                    session.pop('request_attempt')
                return redirect(url_for('show_all_requests'))
            session['request_attempt'] = request.form
        return redirect('/add_request')
    return redirect('/dashboard')

@app.get('/request/<int:request_id>/delete')
def delete_request(request_id:int) -> None:
    if session.get('logged_in'):
        ride_request.Request.delete_one(request_id)
        return redirect(url_for('show_all_requests'))
    return redirect('/')

@app.route('/request/<int:request_id>/edit', methods=["GET", "POST"])
def edit_request(request_id:int) -> None:
    this_request = ride_request.Request.get_one_with_booking(request_id)
    if not this_request:
        return redirect(url_for('show_all_requests'))
    if session.get('logged_in'):
        if request.method == "GET":
            if session.get('edit_attempt'):
                pre_fill = {
                    'driver' : this_request.driver.first_name,
                    'destination': this_request.destination,
                    'date': this_request.date,
                    'pickup': session['edit_attempt']['pickup'],
                    'details': session['edit_attempt']['details'],
                }
            else:
                pre_fill = {
                    'driver' : this_request.driver.first_name,
                    'destination': this_request.destination,
                    'date': this_request.date,
                    'pickup': this_request.pickup,
                    'details': this_request.details,
                }
            return render_template('edit_request.html', pre_fill = pre_fill, request_id = request_id)
        elif request.method == "POST":
            if ride_request.Request.is_legit_request(request.form):
                updated_request = ride_request.Request.update_one(request.form)
                if session.get('edit_attempt'):
                    session.pop('edit_attempt')
                return redirect(url_for('show_all_requests'))
            session['edit_attempt'] = request.form
        return redirect(url_for('edit_request', request_id = request_id))
    return redirect('/')

@app.get('/request/<int:request_id>/edit/link')
def edit_request_from_link(request_id:int) -> None:
    if session.get('edit_attempt'):
        session.pop('edit_attempt')
    return redirect(url_for('edit_request', request_id = request_id))