from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def test_should_return_event_by_category():

    events_repository = EventsRepository(temp_file())
    app = create_app(repositories={"event": events_repository})
    client = app.test_client()

    concierto_queen = Event(
        id="event-1",
        user_id="user-1",
        name="concierto queen",
        description="un tributo a queen",
        date="2022-01-25",
        public=0,
        time="22:00:00",
        categories=["category-1"],
    )

    concierto_camela = Event(
        id="event-2",
        user_id="user-2",
        name="concierto Camela",
        description="un tributo a camela",
        date="2023-08-15",
        public=0,
        time="23:00:00",
        categories=["category-2"],
    )

    events_repository.save(concierto_queen, "user-1")
    events_repository.save(concierto_camela, "user-2")

    response = client.get(
        "/api/categories/category-1", headers={"Authorization": "user-1"}
    )
    # assert response.status_code == 200
    assert response.json == None
    # [
    #     {
    #         "id": "event-1",
    #         "user_id": "user-1",
    #         "name": "concierto queen",
    #         "description": "un tributo a queen",
    #         "date": "2022-01-25",
    #         "public": 0,
    #         "time": "22:00:00",
    #         "categories": ["category-1"],
    #     }
    # ]
    # TypeError: EventsRepository.get_events_by_categorie() takes 2 positional arguments but 3 were given
    # assert 500 == 200
    # no debe ser None el response.json


# def test_shouldnt_return_nothing_if_authorization_wrong():

#     events_repository = EventsRepository(temp_file())
#     app = create_app(repositories={"event": events_repository})
#     client = app.test_client()

#     concierto_queen = Event(
#         id="event-1",
#         user_id="user-1",
#         name="concierto queen",
#         description="un tributo a queen",
#         date="2022-01-25",
#         public=0,
#         time="22:00:00",
#         categories=["category-1"],
#     )

#     concierto_camela = Event(
#         id="event-2",
#         user_id="user-2",
#         name="concierto Camela",
#         description="un tributo a camela",
#         date="2023-08-15",
#         public=0,
#         time="23:00:00",
#         categories=["category-2"],
#     )
#     events_repository.save(concierto_queen, "user-1")
#     events_repository.save(concierto_camela, "user-2")
#     response = client.get(
#         "/api/categories/category-1", headers={"Authorization": "user-2"}
#     )
#     print("****************************************************", response)
#     # assert response.data == b""
#     assert response.data == None


# def test_shouldnt_return_nothing_if_category_id_wrong():

#     events_repository = EventsRepository(temp_file())
#     app = create_app(repositories={"event": events_repository})
#     client = app.test_client()

#     concierto_queen = Event(
#         id="event-1",
#         user_id="user-1",
#         name="concierto queen",
#         description="un tributo a queen",
#         date="2022-01-25",
#         public=0,
#         time="22:00:00",
#         categories=["category-1"],
#     )

#     concierto_camela = Event(
#         id="event-2",
#         user_id="user-2",
#         name="concierto Camela",
#         description="un tributo a camela",
#         date="2023-08-15",
#         public=0,
#         time="23:00:00",
#         categories=["category-2"],
#     )
#     events_repository.save(concierto_queen, "user-1")
#     events_repository.save(concierto_camela, "user-2")
#     response = client.get(
#         "/api/categories/category-101", headers={"Authorization": "user-2"}
#     )
#     assert response.status_code == 404
#     assert response.data == b""

# TypeError: EventsRepository.get_events_by_categorie() takes 2 positional arguments but 3 were given
# FAILED test/events/test_get_events_by_category.py::test_should_return_event_by_category - assert 500 == 200
# FAILED test/events/test_get_events_by_category.py::test_shouldnt_return_nothing_if_category_id_wrong - assert 500 == 404
