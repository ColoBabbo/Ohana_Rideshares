from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Message:
    db = 'ohana_rideshare_schema'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.booking_id = data['booking_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls) -> list[dict]:
        query = "SELECT * FROM messages;"
        results = connectToMySQL(cls.db).query_db(query)
        all_messages = []
        for message in results:
            all_messages.append(cls(message))
        return all_messages

    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO messages (user_id, booking_id, content)
                VALUES (%(user_id)s, %(booking_id)s, %(content)s);
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)


    @classmethod
    def get_all_with_user(cls, booking_id) -> dict[object]:
        query = """
                SELECT * FROM messages
                LEFT JOIN users ON messages.user_id = users.id
                WHERE booking_id = %(booking_id)s
        """
        results = connectToMySQL(cls.db).query_db(query, {'booking_id' : booking_id})
        all_messages = []

        for message in results:
            this_message = cls(message)

            user_data = {
                'id': message['users.id'],
                'first_name': message['first_name'],
                'last_name': message['last_name'],
                'email': message['email'],
                'created_at': message['users.created_at'],
                'updated_at': message['users.updated_at'],
            }
            this_message_user = user.User(user_data)
            this_message.user = this_message_user

            all_messages.append(this_message)
        return all_messages

    @classmethod
    def is_legit_message(cls, form_dict:dict) -> bool:
        valid_input = True
        if not len(form_dict.get('content')) > 0:
                flash('Message cannot be blank.', 'message')
                valid_input = False
        return valid_input

    @classmethod
    def delete_one(cls, message_id:int) -> None:
        query = """
                DELETE FROM messages
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": message_id})

