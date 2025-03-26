import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///muscle_training.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CALENDAR_FIRST_DAY = 0  # 0 = 日曜日始まり