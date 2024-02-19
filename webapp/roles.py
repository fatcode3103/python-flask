from flask import Blueprint, request, jsonify
from . import get_session
from .models import Role
from .models import Permission
from .models import GroupPermission
from sqlalchemy.orm import joinedload
from sqlalchemy import delete

roles = Blueprint("roles", __name__)


def get_all_roles():
    session = get_session()
    all_roles = session.query(Role).options(joinedload(Role.group_permission)).all()
    roles_data = []
    for role in all_roles:
        permissions = [permission.permission_id for permission in role.group_permission]
        role_data = {
            "id": role.id,
            "name": role.name,
            "permissions": permissions,
            "created_at": role.created_at,
            "updated_at": role.updated_at,
        }
        roles_data.append(role_data)
    return roles_data


@roles.route("/roles", methods=["GET"])
def get_roles():
    try:
        session = get_session()
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
        session = get_session()
        name = request.json["name"]
        new_role = Role(name=name)
        session.add(new_role)
        session.commit()
        curr_role_id = new_role.id

        per_id_array = request.json["permission_id"]
        permission_array = [
            GroupPermission(role_id=curr_role_id, permission_id=item)
            for item in per_id_array
        ]
        session.bulk_save_objects(permission_array)
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
        session = get_session()
        role_id = request.args.get("role_id")
        role = session.query(Role).filter_by(id=role_id).first()
        delete_stmt = delete(GroupPermission).where(GroupPermission.role_id == role_id)

        session.execute(delete_stmt)
        ## delete role itself
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
        session = get_session()
        role_id = request.json["role_id"]
        new_permission = request.json["permission_id"]
        new_name = request.json["name"]

        per_by_role = session.query(GroupPermission).filter_by(role_id=role_id).all()
        prev_permissions = [permission.permission_id for permission in per_by_role]

        per_addition = list(set(new_permission) - set(prev_permissions))
        per_remove = list(set(prev_permissions) - set(new_permission))

        ## add new permission
        permission_list = [
            GroupPermission(role_id=role_id, permission_id=item)
            for item in per_addition
        ]
        session.bulk_save_objects(permission_list)

        ## remove permission
        for item in per_remove:
            per_role = (
                session.query(GroupPermission).filter_by(permission_id=item).first()
            )
            session.delete(per_role)

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


def get_all_permissions():
    session = get_session()
    all_permissions = session.query(Permission).all()
    permissions_data = []
    for per_data in all_permissions:
        data = {
            "id": per_data.id,
            "name": per_data.name,
            "created_at": per_data.created_at,
            "updated_at": per_data.updated_at,
        }
        permissions_data.append(data)
    return permissions_data


@roles.route("/permissions", methods=["GET"])
def get_permission():
    try:
        session = get_session()
        permissions_data = get_all_permissions()
        return (
            jsonify(
                {"data": permissions_data, "message": "Get permissions successful"}
            ),
            200,
        )
    except Exception as ex:
        print(f"Error{ex}")
        return jsonify({"message": "Get permissions failed"}), 500
    finally:
        session.close()


@roles.route("/delete-permissions", methods=["DELETE"])
def delete_permission():
    try:
        session = get_session()
        per_id = request.args.get("permission_id")
        permission = session.query(Permission).filter_by(id=per_id).first()
        session.delete(permission)
        session.commit()
        permissions_data = get_all_permissions()
        return (
            jsonify(
                {"data": permissions_data, "message": "Delete permissions successful"}
            ),
            200,
        )
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Delete permissions failed"}), 500
    finally:
        session.close()


@roles.route("/add-permission", methods=["POST"])
def add_permission():
    try:
        session = get_session()
        name = request.json["name"]
        new_permission = Permission(name=name)
        session.add(new_permission)
        session.commit()
        permissions_data = get_all_permissions()
        return (
            jsonify(
                {"data": permissions_data, "message": "Add new permissions successful"}
            ),
            200,
        )
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Add new permissions failed"}), 500
    finally:
        session.close()


@roles.route("/update-permission", methods=["PUT"])
def update_permission():
    try:
        session = get_session()
        new_name = request.json["name"]
        per_id = request.json["permission_id"]
        permission = session.query(Permission).filter_by(id=per_id).first()
        permission.name = new_name
        session.commit()
        permissions_data = get_all_permissions()
        return (
            jsonify(
                {"data": permissions_data, "message": "Update permissions successful"}
            ),
            200,
        )
    except Exception as ex:
        print(f"Error{ex}")
        session.rollback()
        return jsonify({"message": "Update permissions failed"}), 500
    finally:
        session.close()
