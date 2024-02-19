from flask import Blueprint, request, jsonify
from . import get_session
from .models import Role

roles = Blueprint("roles", __name__)

session = get_session()


def get_all_roles():
    all_roles = session.query(Role).all()
    roles_data = []
    for role in all_roles:
        role_data = {
            "id": role.id,
            "name": role.name,
            "created_at": role.created_at,
            "updated_at": role.updated_at,
        }
        roles_data.append(role_data)
    return roles_data


@roles.route("/roles", methods=["GET"])
def get_roles():
    try:
        roles_data = get_all_roles()
        return jsonify({"data": roles_data, "message": "Get roles successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        return jsonify({"message": "Get roles failed"}), 500
    finally:
        session.close()


@roles.route("/add-role", methods=["POST"])
def add_new_role():
    try:
        name = request.json["name"]
        new_role = Role(name=name)
        session.add(new_role)
        session.commit()
        roles_data = get_all_roles()
        return jsonify({"data": roles_data, "message": "Add new role successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Add new role failed"}), 500
    finally:
        session.close()


@roles.route("/delete-role", methods=["DELETE"])
def delete_role():
    try:
        role_id = request.args.get("role_id")
        role = session.query(Role).filter_by(id=role_id).first()
        session.delete(role)
        session.commit()
        roles_data = get_all_roles()
        return jsonify({"data": roles_data, "message": "Delete role successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Delete role failed"}), 500
    finally:
        session.close()


@roles.route("/update-role", methods=["PUT"])
def update_role():
    try:
        role_id = request.json["role_id"]
        new_name = request.json["name"]
        role = session.query(Role).filter_by(id=role_id).first()
        role.name = new_name
        session.commit()
        roles_data = get_all_roles()
        return jsonify({"data": roles_data, "message": "Update role successful"}), 200
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Update role failed"}), 500
    finally:
        session.close()
