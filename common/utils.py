from passlib.hash import pbkdf2_sha512
import secrets
import datetime
import pytz
from flask import jsonify


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def secret_key(length):
        return secrets.token_urlsafe(length)

# ****************************************** datetime_util ************************************************

    @staticmethod
    def tzware_datetime():
        """
        Return a timezone aware datetime.

        :return: Datetime
        """
        return datetime.datetime.now(pytz.utc)

    @staticmethod
    def timedelta_months(months, compare_date=None):
        """
        Return a new datetime with a month offset applied.

        :param months: Amount of months to offset
        :type months: int
        :param compare_date: Date to compare at
        :type compare_date: date
        :return: datetime
        """
        if compare_date is None:
            compare_date = datetime.datetime.today()

        delta = months * 365 / 12
        compare_date_with_delta = compare_date + datetime.timedelta(delta)

        return compare_date_with_delta

    # ******************* currency Dollar to cents ***************
    @staticmethod
    def cents_to_dollars(cents):
        """
        Convert cents to dollars.

        :param cents: Amount in cents
        :type cents: int
        :return: float
        """
        return round(cents / 100.0, 2)

    @staticmethod
    def dollars_to_cents(dollars):
        """
        Convert dollars to cents.

        :param dollars: Amount in dollars
        :type dollars: float
        :return: int
        """
        return int(dollars * 100)

    @staticmethod
    def render_json(status, *args, **kwargs):
        """
        Return a JSON response.

        Example usage:
          render_json(404, {'error': 'Discount code not found.'})
          render_json(200, {'data': coupon.to_json()})

        :param status: HTTP status code
        :type status: int
        :param args:
        :param kwargs:
        :return: Flask response
        """
        response = jsonify(*args, **kwargs)
        response.status_code = status

        return response
