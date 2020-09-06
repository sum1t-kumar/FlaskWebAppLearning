
from models.user.user import User
import models.user.user_error as UserErrors
from common.flask_mailplus import send_template_message


def deliver_password_reset_email(email, reset_token):

    user = User.find_by_email(email=email)
    try:
        ctx = {'user': user, 'reset_token': reset_token}

        send_template_message(subject='REDFI Password reset',
                              recipients=[email],
                              template='mail/password_reset', ctx=ctx)
    except Exception:
        raise UserErrors.InvalidEmailError("Can't validate the email address provided. Make sure email is correct or try after sometime.")
    return None


def deliver_mail_verification_email(email, mail_verification):

    user = User.find_by_email(email=email)
    try:
        ctx = {'user': user, 'mail_verification': mail_verification}

        send_template_message(subject='REDFI E-mail Verification',
                              recipients=[email],
                              template='mail/mail_verification', ctx=ctx)
    except Exception:
        raise UserErrors.InvalidEmailError("Can't validate the email address provided. Make sure email is correct or try after sometime.")
    return None
