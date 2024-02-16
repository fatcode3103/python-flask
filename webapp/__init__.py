from flask import Flask
from .views import views
from .auth import auth
from sqlalchemy import create_engine

DB_NAME = "database.db"

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'Root123@'
host = 'localhost'
port = 3308
database = 'demo_python_connect_db'

def get_connection():
  return create_engine(
    url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )
  )

def create_app():
  app = Flask(__name__)
  try:
      
      engine = get_connection()
      print(
          f"Connection to the {host} for user {user} created successfully.")
  except Exception as ex:
      print("Connection could not be made due to the following error: \n", ex)

  app.register_blueprint(views, url_prefix="/view")
  app.register_blueprint(auth, url_prefix="/auth")

  return app

