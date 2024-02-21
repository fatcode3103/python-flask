from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload, contains_eager

from .models import User
from .models import Role
from . import get_session

users = Blueprint("users", __name__)


def get_users_with_roles_data():
    session = get_session()
    users_with_roles_and_permission = (
        session.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.role).joinedload(Role.group_permission),
        )
        .all()
    )

    users_data = []
    for user in users_with_roles_and_permission:
        permissions = (
            [permission.permission_id for permission in user.role.group_permission]
            if user.role
            else None
        )
        user_data = {
            "id": user.id,
            "name": user.name,
            "role_id": user.role_id,
            "role_name": user.role.name if user.role else None,
            "permission": permissions,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        users_data.append(user_data)
    return users_data


@users.route("/users", methods=["GET"])
def get_users():
    session = get_session()
    try:
        users_data = get_users_with_roles_data()
        return jsonify({"data": users_data, "message": "Get users successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        return jsonify({"message": "Get users failed"}), 500
    finally:
        session.close()


@users.route("/add-user", methods=["POST"])
def add_user():
    session = get_session()
    try:
        new_user = User(name=request.json["name"], role_id=request.json["role_id"])
        session.add(new_user)
        session.commit()
        crr_user = {"name": new_user.name, "role_id": new_user.role_id}
        return (
            jsonify({"data": crr_user, "message": "Create new user successful"}),
            200,
        )
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Add new failed"}), 500
    finally:
        session.close()


@users.route("/delete-user", methods=["DELETE"])
def delete_user():
    session = get_session()
    try:
        user_id = request.args.get("user_id")
        user = session.query(User).filter_by(id=user_id).first()
        session.delete(user)
        session.commit()
        users_data = get_users_with_roles_data()
        return jsonify({"data": users_data, "message": "Delete user successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Delete user failed"}), 500
    finally:
        session.close()


@users.route("/update-user", methods=["PUT"])
def update_user():
    session = get_session()
    try:
        user_id = request.json["user_id"]
        user = session.query(User).filter_by(id=user_id).first()
        name = request.json["name"]
        role_id = request.json["role_id"]

        user.name = name
        user.role_id = role_id
        session.commit()
        crr_user = {"name": name, "role_id": role_id}
        return jsonify({"data": crr_user, "message": "Update user successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Update user failed"}), 500
    finally:
        session.close()
