from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import request, user

class Booking:
    db = 'ohana_rideshare_schema'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.request_id = data['request_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.driver = {}
        self.passenger = {}
        self.request = {}

    @classmethod
    def get_all(cls) -> list[dict]:
        query = "SELECT * FROM bookings;"
        results = connectToMySQL(cls.db).query_db(query)
        all_bookings = []
        for booking in results:
            all_bookings.append(cls(booking))
        return all_bookings

    @classmethod
    def get_all_with_driver(cls) -> dict[object]:
        query = """
                SELECT * FROM bookings
                LEFT JOIN users AS drivers ON bookings.user_id = drivers.id
                LEFT JOIN requests ON bookings.request_id = requests.id
                LEFT JOIN users AS passengers ON requests.user_id = passengers.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_bookings = {}

        for booking in results:
            this_booking = cls(booking)

            driver_data = {
                'id': booking['drivers.id'],
                'first_name': booking['first_name'],
                'last_name': booking['last_name'],
                'email': booking['email'],
                'created_at': booking['drivers.created_at'],
                'updated_at': booking['drivers.updated_at'],
            }
            this_booking_driver = user.User(driver_data)
            this_booking.driver = this_booking_driver

            request_data = {
                'id': booking['requests.id'],
                'user_id': booking['requests.user_id'],
                'destination': booking['destination'],
                'pickup': booking['pickup'],
                'date': booking['date'],
                'details': booking['details'],
                'created_at': booking['requests.created_at'],
                'updated_at': booking['requests.updated_at'],
            }
            this_booking_request = request.Request(request_data)
            this_booking.request = this_booking_request
            
            passenger_data = {
                'id': booking['passengers.id'],
                'first_name': booking['passengers.first_name'],
                'last_name': booking['passengers.last_name'],
                'email': booking['passengers.email'],
                'created_at': booking['passengers.created_at'],
                'updated_at': booking['passengers.updated_at'],
            }
            this_booking_passenger = user.User(passenger_data)
            this_booking.passenger = this_booking_passenger

            all_bookings[this_booking.request.id] = (this_booking)
        return all_bookings

    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO bookings (user_id, request_id)
                VALUES (%(user_id)s, %(request_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def is_legit_booking(cls, form_dict:dict) -> bool:
        valid_input = True
        all_bookings = cls.get_all()
        for booking in all_bookings:
            if form_dict['request_id'] == str(booking.request_id):
                flash('This ride is already booked.', 'booking')
                valid_input = False
                return valid_input
        return valid_input

    @classmethod
    def delete_one(cls, booking_id:int) -> None:
        query = """
                DELETE FROM bookings
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": booking_id})

