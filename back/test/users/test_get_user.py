from urllib import response
from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.users import UsersRepository, User


def test_should_return_empty_list_of_users():

    users_repository = UsersRepository(temp_file())
    app = create_app(repositories={"user": users_repository})
    client = app.test_client()

    response = client.get("/api/users")

    assert response.json == []


def test_should_return_user_in_database():

    users_repository = UsersRepository(temp_file())
    app = create_app(repositories={"user": users_repository})
    client = app.test_client()

    camelia = User(
        id="user-1",
        user_name="camelia",
    )
    users_repository.save(camelia)

    response = client.get("/api/users")

    assert response.json == [
        {
            "id": "user-1",
            "user_name": "camelia",
        }
    ]
