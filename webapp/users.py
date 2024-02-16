from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import User

users = Blueprint("users", __name__)

def get_session():
  user = 'root'
  password = 'Root_12345'
  host = 'localhost'
  database = 'demo_python_connect_db'

  engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
  Session = sessionmaker(bind=engine)
  session = Session()
  return session

session = get_session()

@users.route("/users", methods=['GET'])
def get_users():
  try:
    all_users = session.query(User).all()
    session.close()

    users_data = []
    for user in all_users:
      user_data = {
        'id': user.id,
        'name': user.name,
        'role_id': user.role_id,
        'created_at': user.created_at,
        'updated_at': user.updated_at
      }
      users_data.append(user_data)

      
    return jsonify({"data": users_data, "message": "Get users successful"})
  except Exception as ex:
    print(f"Error{ex}")
    return jsonify({"message": "Get users failed"}), 500
  finally:
    session.close()

@users.route("/add-user", methods=['POST'])
def add_user():
  try:
    new_user = User(name=request.json["name"], role_id=request.json["role_id"])
    session.add(new_user)
    session.commit()
    return jsonify({"data": "", "message": "Create new user successful"})
  except Exception as ex:
    print(f"Error{ex}")
    session.rollback()
    return jsonify({"message": "Add new failed"}), 500
  finally:
    session.close()
