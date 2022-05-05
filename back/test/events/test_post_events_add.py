from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event
from src.domain.categories import CategoryRepository, Category


def test_front_should_post_new_events():
    category_repository = CategoryRepository(temp_file())
    events_repository = EventsRepository(temp_file())
    app = create_app(
        repositories={"event": events_repository, "category": category_repository}
    )
    client = app.test_client()

    body = {
        "id": "event-1",
        "name": "concierto queen",
        "description": "un tributo a queen",
        "date": "2022-01-25",
        "public": 0,
        "time": "22:00:00",
        "categories": ["category-1"],
    }

    client.post("/api/events", json=body, headers={"Authorization": "user-1"})

    response_get = client.get(
        "/api/events/event-1", headers={"Authorization": "user-1"}
    )

    assert response_get.json == {
        "id": "event-1",
        "user_id": "user-1",
        "name": "concierto queen",
        "description": "un tributo a queen",
        "date": "2022-01-25",
        "public": 0,
        "time": "22:00:00",
        "categories": [],
    }
