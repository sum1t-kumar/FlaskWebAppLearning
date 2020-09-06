import os

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = 'SecureKey'

MAIL_DEFAULT_SENDER = 'sumit.redfi@gmail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'sumit.redfi@gmail.com'
MAIL_PASSWORD = '********'

basedir = os.path.abspath(os.path.dirname(__file__))

EXPORT_PATH = os.path.join(basedir, 'exports')
