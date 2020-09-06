
from functools import wraps

from flask import session, flash, redirect, url_for, request


def requires_login(f: object) -> object:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash(u'You need to be sign in for this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function

