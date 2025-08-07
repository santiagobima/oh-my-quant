import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DEBUG = os.getenv('DEBUG') == 'True' #--->> Lo convierto a booleano
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    API_KEY = os.getenv('API_KEY')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    
    