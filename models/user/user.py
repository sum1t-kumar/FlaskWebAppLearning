import uuid
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
from flask import current_app
from common.database import Database
import models.user.user_error as UserErrors
from common.utils import Utils


class User(object):
    COLLECTION = "users"
    
    def __init__(self, email, password, name=None, company=None, email_valid=None, _id=None, role='member', image='https://image.flaticon.com/icons/svg/599/599305.svg'):
        self.email = email
        self.password = Utils.hash_password(password)
        self.name = name
        self.company = company
        self.email_valid = email_valid
        self._id = uuid.uuid4().hex if _id is None else _id
        self.role = role
        self.image = image

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "email_valid": self.email_valid,
            "company": self.company,
            "role": self.role,
            "image": self.image
        }

    def save_to_db(self):
        Database.insert(self.COLLECTION, self.json())

    def update_user(self):
        Database.update(self.COLLECTION, query={'_id': self._id}, data={'$set': self.json()})

    def register_user(self):

        user_data = Database.find_one(User.COLLECTION, {"email": self.email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        self.save_to_db()
        return True

    @staticmethod
    def login(email, password):
        user_data = Database.find_one(User.COLLECTION, {"email": email})

        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist. Try sign up!")

        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("E-mail or password is incorrect.")
        return True

    @classmethod
    def find_by_email(cls, email):
        user_data = Database.find_one(User.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Invalid username")
        return cls(**Database.find_one(User.COLLECTION, {'email': email}))

    @classmethod
    def find_by_id(cls, _id):
        user_data = Database.find_one(User.COLLECTION, {"_id": _id})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Invalid username")
        return cls(**Database.find_one(User.COLLECTION, {'_id': _id}))

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            return User.find_by_email(email=decoded_payload.get('email'))
        except Exception as e:
            return None

    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)
        return serializer.dumps({'email': self.email}).decode('utf-8')


