from unittest.mock import patch
from webapp.models import User


def test_get_all_users(client, app, db_session):
    # mock data
    user1 = User(name="John", role_id=1)
    user2 = User(name="Jane", role_id=2)
    with patch("webapp.users.get_session", return_value=db_session):
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        response = client.get("/users")

    assert response.status_code == 200
    assert response.json["message"] == "Get users successful"
    assert len(response.json["data"]) == 2
    assert response.json["data"][0]["name"] == "John"
    assert response.json["data"][0]["role_id"] == 1
    assert response.json["data"][1]["name"] == "Jane"
    assert response.json["data"][1]["role_id"] == 2


def test_can_add_new_user(client, app, db_session):
    mock_data = {
        "name": "John",
        "role_id": 1,
    }

    with patch("webapp.users.get_session", return_value=db_session):
        response = client.post("/add-user", json=mock_data)
        user = response.json["data"]
        message = response.json["message"]
    assert user == mock_data
    assert message == "Create new user successful"


def test_can_delete_user(client, app, db_session):
    # init data
    user = User(name="John", role_id=1)
    db_session.add(user)
    db_session.commit()

    crr_user_id = user.id

    with patch("webapp.users.get_session", return_value=db_session):
        response = client.delete(f"/delete-user?user_id={crr_user_id}")

    assert response.status_code == 200
    assert response.json["message"] == "Delete user successful"

    deleted_user = db_session.query(User).filter_by(id=crr_user_id).first()
    assert deleted_user is None


def test_can_update_user(client, app, db_session):
    # init data
    user1 = User(name="Jey", role_id=2)
    user = User(name="Jack", role_id=2)
    db_session.add(user1)
    db_session.commit()
    data = {"name": user.name, "role_id": user.role_id, "user_id": 1}

    with patch("webapp.users.get_session", return_value=db_session):
        response = client.put("/update-user", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Update user successful"

    ## get user date after updated
    updated_user = db_session.query(User).filter_by(id=data["user_id"]).first()
    assert updated_user.name == "Jack"
    assert updated_user.role_id == 2
