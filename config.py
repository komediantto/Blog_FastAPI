import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY')
USER_SECRET_KEY = os.getenv('USER_SECRET_KEY')
EMAIL_API = os.getenv('EMAIL_API')
