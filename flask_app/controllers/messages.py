from flask import redirect, request, url_for
from flask_app import app
from flask_app.models import message


@app.post('/add_message')
def add_message():
    if message.Message.is_legit_message(request.form):
        new_message = message.Message.insert_one(request.form)
    return redirect(url_for('show_one_request', request_id = request.form['request_id']))
