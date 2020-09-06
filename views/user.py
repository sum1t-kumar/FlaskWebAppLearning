from flask import Blueprint, session, render_template, flash, redirect, url_for, request
from models.user.user import User
from models.user.tasks import deliver_mail_verification_email
import models.user.user_error as UserErrors
from models.user.forms import LoginForm, RegistrationForm, MailVerifiedForm, PasswordResetForm, PasswordResetTriggerForm
from models.user.decorators import requires_login

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        # email = request.form.get('email')
        # password = request.form.get('password')
        email = form.email.data
        password = form.password.data
        try:
            if User.login(email, password):
                session['email'] = email
                return redirect(url_for('home_page'))
        except UserErrors.UserError as e:
            session['email'] = None
            flash(e.message, 'danger')
    return render_template("login.html", form=form)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(form.email.data, form.password.data, form.name.data, form.company.data)
        try:
            user.register_user()
            session['email'] = user.email
            flash('Sign up is complete, enjoy our services. \nAn E-mail address verification link has been sent to {0}.'.format(form.email.data), 'success')
            return redirect(url_for('users.mail_verification'))
        except UserErrors.UserAlreadyRegisteredError as e:
            flash(e.message, 'danger')
    return render_template('signup.html', form=form)


@users.route('/mail/verification', methods=['GET', 'POST'])
def mail_verification():
    email = session['email']
    user = User.find_by_email(email=email)
    mail_verification = user.serialize_token()
    deliver_mail_verification_email(email=email, mail_verification=mail_verification)
    return redirect(url_for('home_page'))


@users.route('mail/verified', methods=['GET', 'POST'])
def mail_verified():
    form = MailVerifiedForm(mail_verification=request.args.get('mail_verification'))
    if form.validate_on_submit():
        user = User.deserialize_token(request.form.get('mail_verification'))
        if user is None:
            flash('Your mail verification has expired or was tampered with.', 'danger')
            return redirect(url_for('users.login_user'))
        user.email_valid = True
        user.update_user()
        flash('Your E-mail address has been verified', 'success')
        return redirect(url_for('users.login_user'))

    return render_template('mail_verification.html', form=form)


@users.route('/logout')
@requires_login
def logout_user():
    session['email'] = None
    return redirect(url_for('home_page'))


@users.route('/reset', methods=['GET', 'POST'])
def password_reset_trigger():
    form = PasswordResetTriggerForm()

    if form.validate_on_submit():
        email = form.email.data
        try:
            user = User.find_by_email(email=email)
            reset_token = user.serialize_token()
            from models.user.tasks import deliver_password_reset_email
            deliver_password_reset_email(email, reset_token)
            flash('A password rest link has been sent to {0}.'.format(email), 'success')
            return redirect(url_for('users.login_user'))
        except UserErrors.UserError as e:
            flash(e.message, 'danger')
    return render_template('password_reset_trigger.html', form=form)


@users.route('/reset/reset', methods=['GET', 'POST'])
def password_reset():
    form = PasswordResetForm(reset_token=request.args.get('reset_token'))
    if form.validate_on_submit():
        user = User.deserialize_token(request.form.get('reset_token'))
        if user is None:
            flash('Your reset token has expired or was tampered with.', 'danger')
            return redirect(url_for('users.password_reset_trigger'))

        form.populate_obj(user)
        hashed_password = User(email='None', password=request.form.get('password')).password  # hack to encrypt a password. by running init
        user.password = hashed_password
        user.update_user()

        flash('Your password has been reset.', 'success')
        return redirect(url_for('users.login_user'))

    return render_template('password_reset.html', form=form)


@users.route('/settings')
@requires_login
def settings():
    return render_template('settings.html')

