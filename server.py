from flask_app import app
from flask_app.controllers import users, requests, bookings, messages

if __name__ == "__main__":
    app.run(debug=True)


# New change