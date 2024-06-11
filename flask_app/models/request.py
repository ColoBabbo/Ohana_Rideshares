from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, booking, message

class Request:
    db = 'ohana_rideshare_schema'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.destination = data['destination']
        self.pickup = data['pickup']
        self.date = data['date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.passenger = None
        self.driver = None
        self.booking = None
        self.messages = []

    @classmethod
    def get_all(cls) -> list[object]:
        query = "SELECT * FROM requests;"
        results = connectToMySQL(cls.db).query_db(query)
        all_requests = []
        for request in results:
            all_requests.append(cls(request))
        print(all_requests)
        return all_requests

    @classmethod
    def get_all_with_booking(cls) -> dict[object]:
        query = """
                SELECT * FROM requests
                LEFT JOIN users AS passengers ON requests.user_id = passengers.id
                LEFT JOIN bookings ON bookings.request_id = requests.id
                LEFT JOIN users AS drivers ON bookings.user_id = drivers.id
                LEFT JOIN messages ON booking_id = bookings.id
                LEFT JOIN users ON messages.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_requests =  {}

        for each_request in results:
            if each_request['id'] not in all_requests:
                this_request = cls(each_request)

                passenger_data = {
                    'id': each_request['passengers.id'],
                    'first_name': each_request['first_name'],
                    'last_name': each_request['last_name'],
                    'email': each_request['email'],
                    'created_at': each_request['passengers.created_at'],
                    'updated_at': each_request['passengers.updated_at'],
                }
                this_request_passenger = user.User(passenger_data)
                this_request.passenger = this_request_passenger

                booking_data = {
                    'id': each_request['bookings.id'],
                    'user_id': each_request['bookings.user_id'],
                    'request_id': each_request['request_id'],
                    'created_at': each_request['bookings.created_at'],
                    'updated_at': each_request['bookings.updated_at'],
                }
                this_request_booking = booking.Booking(booking_data)
                this_request.booking = this_request_booking

                driver_data = {
                    'id': each_request['drivers.id'],
                    'first_name': each_request['drivers.first_name'],
                    'last_name': each_request['drivers.last_name'],
                    'email': each_request['drivers.email'],
                    'created_at': each_request['drivers.created_at'],
                    'updated_at': each_request['drivers.updated_at'],
                }
                this_request_driver = user.User(driver_data)
                this_request.driver = this_request_driver

                message_data = {
                    'id': each_request['messages.id'],
                    'user_id': each_request['messages.user_id'],
                    'booking_id': each_request['booking_id'],
                    'content': each_request['content'],
                    'created_at': each_request['messages.created_at'],
                    'updated_at': each_request['messages.updated_at'],
                }
                this_request_message = message.Message(message_data)
                
                this_request_message_user_data = {
                    'id': each_request['users.id'],
                    'first_name': each_request['users.first_name'],
                    'last_name': each_request['users.last_name'],
                    'email': each_request['users.email'],
                    'created_at': each_request['users.created_at'],
                    'updated_at': each_request['users.updated_at'],
                }
                this_request_message_user = user.User(this_request_message_user_data)
                this_request_message.user = this_request_message_user
                
                this_request.messages.append(this_request_message)

                all_requests[this_request.id] = (this_request)

            else:
                message_data = {
                    'id': each_request['messages.id'],
                    'user_id': each_request['messages.user_id'],
                    'booking_id': each_request['booking_id'],
                    'content': each_request['content'],
                    'created_at': each_request['messages.created_at'],
                    'updated_at': each_request['messages.updated_at'],
                }
                existing_request_message = message.Message(message_data)
                
                existing_request_message_user_data = {
                    'id': each_request['users.id'],
                    'first_name': each_request['users.first_name'],
                    'last_name': each_request['users.last_name'],
                    'email': each_request['users.email'],
                    'created_at': each_request['users.created_at'],
                    'updated_at': each_request['users.updated_at'],
                }
                existing_request_message_user = user.User(existing_request_message_user_data)
                existing_request_message.user = existing_request_message_user
                
                all_requests[each_request['id']].messages.append(existing_request_message)

        return all_requests


    @classmethod
    def get_one_with_booking(cls, request_id:int) -> object:
        all_requests = cls.get_all_with_booking()
        this_request = all_requests[request_id]
        return this_request

        # query = """
        #         SELECT * FROM requests
        #         LEFT JOIN users AS passengers ON requests.user_id = passengers.id
        #         LEFT JOIN bookings ON bookings.request_id = requests.id
        #         LEFT JOIN users AS drivers ON bookings.user_id = drivers.id
        #         WHERE requests.id = %(id)s
        # """
        # results = connectToMySQL(cls.db).query_db(query, {'id' : request_id})
        # this_request = cls(results[0])

        # passenger_data = {
        #     'id': results[0]['passengers.id'],
        #     'first_name': results[0]['first_name'],
        #     'last_name': results[0]['last_name'],
        #     'email': results[0]['email'],
        #     'created_at': results[0]['passengers.created_at'],
        #     'updated_at': results[0]['passengers.updated_at'],
        # }
        # this_request_passenger = user.User(passenger_data)
        # this_request.passenger = this_request_passenger

        # booking_data = {
        #     'id': results[0]['bookings.id'],
        #     'user_id': results[0]['bookings.user_id'],
        #     'request_id': results[0]['request_id'],
        #     'created_at': results[0]['bookings.created_at'],
        #     'updated_at': results[0]['bookings.updated_at'],
        # }
        # this_request_booking = booking.Booking(booking_data)
        # this_request.booking = this_request_booking

        # driver_data = {
        #     'id': results[0]['drivers.id'],
        #     'first_name': results[0]['drivers.first_name'],
        #     'last_name': results[0]['drivers.last_name'],
        #     'email': results[0]['drivers.email'],
        #     'created_at': results[0]['drivers.created_at'],
        #     'updated_at': results[0]['drivers.updated_at'],
        # }
        # this_request_driver = user.User(driver_data)
        # this_request.driver = this_request_driver

        # return this_request

    @classmethod
    def get_one(cls, request_id:int) -> object:
        query = """
                SELECT * FROM requests
                WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': request_id})
        return cls(results[0])

    @classmethod
    def update_one(cls, form_dict:dict) -> None:
        query = """
                UPDATE requests
                SET destination = %(destination)s, details =  %(details)s, pickup = %(pickup)s, date = %(date)s
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO requests (destination, details, pickup, date, user_id)
                VALUES (%(destination)s, %(details)s, %(pickup)s, %(date)s, %(user_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def delete_one(cls, request_id:int) -> None:
        query = """
                DELETE FROM requests
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": request_id})

    @classmethod
    def is_legit_request(cls, form_dict:dict) -> bool:
        valid_input = True
        if not len(form_dict.get('destination')) > 0 :
            flash('Your request needs a Destination!', 'destination')
            valid_input = False
        elif not len(form_dict.get('destination')) >= 3:
            flash('Destination must be at least 3 characters.', 'destination')
            valid_input = False
        if not len(form_dict.get('details')) > 0 :
            flash('Please add Details to your ride request.', 'details')
            valid_input = False
        elif not len(form_dict.get('details')) >= 10:
            flash('Details must be at least 10 characters.', 'details')
            valid_input = False
        if not len(form_dict.get('pickup')) > 0 :
            flash('Please add Pickup Location.', 'pickup')
            valid_input = False
        elif not len(form_dict.get('pickup')) >= 3:
            flash('Pickup must be at least 3 characters.', 'pickup')
            valid_input = False
        if not form_dict.get('date'):
            flash('Please input ride Date', 'date')
            valid_input = False
        return valid_input