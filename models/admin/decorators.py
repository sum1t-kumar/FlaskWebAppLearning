
from functools import wraps

from flask import session, flash, redirect, url_for
from models.user.user import User


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.find_by_email(email=session['email'])
            if user.role not in roles:
                flash('You do not have permission to do that.', 'error')
                return redirect('/')

            return f(*args, **kwargs)

        return decorated_function

    return decorator

