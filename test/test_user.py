from unittest.mock import patch
from datetime import datetime
import json


def test_get_all_user(client, app):
    mock_data = [
        {
            "name": "John",
            "id": 1,
            "permission": [1, 3],
            "role_id": 1,
            "role_name": "Admin",
            "created_at": "Fri, 16 Feb 2024 16:41:46 GMT",
            "updated_at": "Fri, 16 Feb 2024 16:41:46 GMT",
        }
    ]

    with patch("webapp.users.get_users_with_roles_data", return_value=mock_data):
        response = client.get("/users")
        users = response.json["data"]
        message = response.json["message"]
        assert users == mock_data
        assert message == "Get users successful"


def test_can_add_new_user(client, app):
    mock_data = {
        "name": "John",
        "role_id": 1,
    }

    with patch("webapp.users.get_users_with_roles_data", return_value=mock_data):
        response = client.post("/add-user", json=mock_data)
        user = response.json["data"]
        message = response.json["message"]
        assert user == mock_data
        assert message == "Create new user successful"


# def test_can_delete_user(client):
#     with patch("webapp.users.get_users_with_roles_data", return_value=""):
#         response = client.delete("/delete-user?user_id=1")
# user = response.json["data"]
# message = response.json["message"]
# assert user == mock_data
# assert message == "Create new user successful"
