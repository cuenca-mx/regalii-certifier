import os

from regalii.configuration import Configuration
from regalii.regaliator import Regaliator


API_KEY = os.environ['REGALII_API_KEY']
SECRET_KEY = os.environ['REGALII_SECRET_KEY']
HOST = 'api.casiregalii.com'
VERSION = '3.1'

config = Configuration(API_KEY, SECRET_KEY, HOST, version=VERSION)
client = Regaliator(config)
