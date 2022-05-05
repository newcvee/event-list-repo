from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event
from src.domain.categories import Category, CategoryRepository


def test_get_public_events_should_return_only_public_events():
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
        description="un tributo a queen de la ostia",
        date="2022-01-25",
        public=1,
        time="22:00:00",
        categories=["category-1"],
    )
    events_repository.save(concierto_queen, "user-1")
    response = client.get("api/events/publicevents")
    print("******************************************=>", response)

    assert response.json == [
        {
            "id": "event-1",
            "user_id": "user-1",
            "name": "concierto queen",
            "description": "un tributo a queen de la ostia",
            "date": "2022-01-25",
            "public": 1,
            "time": "22:00:00",
            "categories": [],
        }
    ]


def test_shouldnt_return_nothing_if_event_not_public():
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
        description="un tributo a queen de la ostia",
        date="2022-01-25",
        public=0,
        time="22:00:00",
        categories="category-1",
    )
    events_repository.save(concierto_queen, "user-1")
    response = client.get("api/events/publicevents")

    assert response.json == []


def test_shouldnt_return_nothing_if_the_path_incorrect():
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
        description="un tributo a queen de la ostia",
        date="2022-01-25",
        public=0,
        time="22:00:00",
        categories="category-1",
    )
    events_repository.save(concierto_queen, "user-1")
    response = client.get("api/events/publiceventstes")
    response.status_code = 404
    assert response.status_code == 404
