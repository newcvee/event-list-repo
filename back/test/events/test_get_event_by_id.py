from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.events import EventsRepository, Event
from src.domain.categories import Category, CategoryRepository


def test_should_return_event_by_id():

    category_repository = CategoryRepository(temp_file())
    events_repository = EventsRepository(temp_file())
    app = create_app(
        repositories={"event": events_repository, "category": category_repository}
    )
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
        categories=["category-1"],
    )

    events_repository.save(concierto_queen, "user-1")
    events_repository.save(concierto_camela, "user-2")

    response_queen_for_user1 = client.get(
        "/api/events/event-1", headers={"Authorization": "user-1"}
    )

    assert response_queen_for_user1.status_code == 200
    concierto_queen = response_queen_for_user1.json
    print(concierto_queen)
    assert concierto_queen["id"] == "event-1"
    assert concierto_queen["name"] == "concierto queen"
    assert concierto_queen["user_id"] == "user-1"
    assert concierto_queen["categories"] == []


def test_shouldnt_return_event_by_id_no_authorization():
    category_repository = CategoryRepository(temp_file())
    events_repository = EventsRepository(temp_file())
    app = create_app(
        repositories={"event": events_repository, "category": category_repository}
    )
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

    events_repository.save(concierto_queen, "user-1")

    response = client.get("/api/events/event-1", headers={"Authorization": "user-2"})
    response.status_code = 400
    assert response.status_code == 400


def test_shouldnt_return_event_if_id_wrong():
    category_repository = CategoryRepository(temp_file())
    events_repository = EventsRepository(temp_file())
    app = create_app(
        repositories={"event": events_repository, "category": category_repository}
    )
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
    events_repository.save(concierto_queen, "user-1")
    response = client.get("/api/events/event-101", headers={"Authorization": "user-1"})
    response.status_code = 400
    print(response.json)
    assert response.status_code == 400
