from flask import Flask
from .users import users
from .roles import roles
from sqlalchemy import create_engine
import asyncio

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'Root_12345'
host = 'localhost'
database = 'demo_python_connect_db'

def get_connection():
  return create_engine(
    url="mysql+pymysql://{0}:{1}@{2}/{3}".format(
        user, password, host, database
    )
  )

def create_app():
  app = Flask(__name__)
  try:
    global engine
    engine = get_connection()
    print(
      f"Connection to the {host} for user {user} created successfully.")
  except Exception as ex:
    print("Connection could not be made due to the following error: \n", ex)

  app.register_blueprint(users, url_prefix="/")
  app.register_blueprint(roles, url_prefix="/")

  return app
