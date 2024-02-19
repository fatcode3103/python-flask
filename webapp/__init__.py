from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DEFINE THE DATABASE CREDENTIALS
user = "root"
password = "Root_12345"
host = "localhost"
database = "demo_python_connect_db"


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}/{3}".format(user, password, host, database)
    )


def get_engine():
    return get_connection()


def create_app():
    from .users import users
    from .roles import roles

    app = Flask(__name__)
    try:
        engine = get_engine()
        if engine:
            print(f"Connection to the {host} for user {user} created successfully.")
        else:
            raise Exception("Error connecting")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(roles, url_prefix="/")

    return app


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
