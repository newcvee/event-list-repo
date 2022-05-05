from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def test_delete_method_should_delete_event_by_id():

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
    events_repository.save(concierto_queen, "user_1")
    client.delete("api/events/event-1")

    response = client.get("api/events", headers={"Authorization": "user-1"})

    assert response.status_code == 200
    assert response.json == []


def test_delete_method_should_delete_event_by_id_unauthorized():

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
    events_repository.save(concierto_queen, "user-1")

    response_delete = client.delete(
        "api/events/event-1", headers={"Authorization": "user-2"}
    )
    response = client.get("api/events", headers={"Authorization": "user-1"})

    assert response_delete.status_code == 500
    response_event = response.json

    assert response_event[0]["id"] == "event-1"
    assert response_event[0]["user_id"] == "user-1"
    assert response_event[0]["name"] == "concierto queen"
    assert response_event[0]["categories"] == []
