from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import EmailField, Email


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])


class RegistrationForm(FlaskForm):
    name = StringField('Your Name', [validators.Length(min=1, max=25), validators.DataRequired()])
    company = StringField('Your Company', [validators.Length(min=2, max=25), validators.DataRequired()])
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField('New Password', [validators.DataRequired()])
    # confirm = PasswordField('Repeat Password')


class MailVerifiedForm(FlaskForm):
    mail_verification = HiddenField()


class PasswordResetTriggerForm(FlaskForm):
    email = EmailField('Your email', validators=[DataRequired(), Length(3, 254)])


class LoginForm(FlaskForm):
    next = HiddenField()
    email = EmailField(validators=[DataRequired(), Length(3, 254)])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField('Stay signed in')
    pass

