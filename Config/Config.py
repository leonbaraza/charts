import os

class Development():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Leon@1996@127.0.0.1:5432/sales_demo'
    SECRET_KEY = '11ae8fcaceff9710e238b932e95072a1'
    DEBUG = True