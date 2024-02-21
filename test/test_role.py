from unittest.mock import patch
from urllib import response
from webapp.models import Role, Permission, GroupPermission


def test_can_get_all_roles(client, app, db_session):
    role = Role(name="Viewer")
    db_session.add(role)
    db_session.commit()
    with patch("webapp.roles.get_session", return_value=db_session):

        response = client.get("/roles")

        data = response.json["data"]
        message = response.json["message"]
        assert response.status_code == 200
        assert len(data) == 3
        assert data[2]["name"] == "Viewer"
        assert message == "Get roles successful"


def test_can_add_new_user(client, app, db_session):
    mock_data = {
        "name": "Viewer",
        "permission_id": [2],
    }
    with patch("webapp.roles.get_session", return_value=db_session):
        response = client.post("/add-role", json=mock_data)
        role = response.json["data"]
        message = response.json["message"]
    assert role == mock_data
    assert message == "Add new role successful"


def test_can_delete_role(client, app, db_session):
    role = Role(name="Viewer")
    db_session.add(role)
    db_session.commit()
    role_id = role.id

    with patch("webapp.roles.get_session", return_value=db_session):
        response = client.delete(f"/delete-role?role_id={role_id}")

    message = response.json["message"]
    assert response.status_code == 200
    assert message == "Delete role successful"

    deleted_role = db_session.query(Role).filter_by(id=role_id).first()
    assert deleted_role is None


def test_can_update_role(client, app, db_session):
    # init data
    data = {"name": "View", "permission_id": [1, 2], "role_id": 2}
    with patch("webapp.roles.get_session", return_value=db_session):
        response = client.put("/update-role", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Update role successful"

    ## get role date after updated
    updated_role = db_session.query(Role).filter_by(id=data["role_id"]).first()
    updated_permissions = (
        db_session.query(GroupPermission).filter_by(role_id=data["role_id"]).all()
    )
    updated_permission_ids = [
        permission.permission_id for permission in updated_permissions
    ]
    assert updated_role.name == data["name"]
    assert set(updated_permission_ids) == set(data["permission_id"])


def test_can_get_all_permission(client, app, db_session):
    role = Permission(name="Delete")
    db_session.add(role)
    db_session.commit()
    with patch("webapp.roles.get_session", return_value=db_session):

        response = client.get("/permissions")

        data = response.json["data"]
        message = response.json["message"]
    assert response.status_code == 200
    assert len(data) == 3
    assert data[2]["name"] == "Delete"
    assert message == "Get permissions successful"


def test_can_add_new_permission(client, app, db_session):
    mock_data = {
        "name": "Delete",
    }
    with patch("webapp.roles.get_session", return_value=db_session):
        response = client.post("/add-permission", json=mock_data)
        role = response.json["data"]
        message = response.json["message"]
    assert role == mock_data
    assert message == "Add new permissions successful"


def test_can_delete_permission(client, app, db_session):
    permission = Permission(name="Delete")
    db_session.add(permission)
    db_session.commit()
    permission_id = permission.id

    with patch("webapp.roles.get_session", return_value=db_session):
        response = client.delete(f"/delete-permissions?permission_id={permission_id}")

    message = response.json["message"]
    assert response.status_code == 200
    assert message == "Delete permissions successful"

    deleted_permission = (
        db_session.query(Permission).filter_by(id=permission_id).first()
    )
    assert deleted_permission is None


def test_can_update_permission(client, app, db_session):
    # init data
    permission1 = Permission(name="Create")
    db_session.add(permission1)
    db_session.commit()
    data = {"name": "ds", "permission_id": 3}

    with patch("webapp.roles.get_session", return_value=db_session):
        response = client.put("/update-permission", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Update permissions successful"

    ## get permission date after updated
    permission = (
        db_session.query(Permission).filter_by(id=data["permission_id"]).first()
    )
    assert permission.name == data["name"]
