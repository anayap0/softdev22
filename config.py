import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = []
    POSTS_PER_PAGE = 25
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.pdf', '.docx', 'zip'] # for file upload   TODO: choose allowed extensions (word docs are seen as zip files?!?!?!)
    MAX_CONTENT_LENGTH = 1024 * 1024 # for file upload
    UPLOAD_PATH = './app/uploads' # for file upload
    UPLOAD_FOLDER = 'uploads' # for file upload