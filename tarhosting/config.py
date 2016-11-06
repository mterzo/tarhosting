"""
Load settings from Environment or set the default value
"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
UPLOAD_FOLDER = os.getenv('TARHOSTING_UPLOAD_DIR', '/tmp')
STATIC_DIR = os.getenv('TARHOSTING_STATIC_DIR', "%s/%s" % (BASEDIR, "static"))
