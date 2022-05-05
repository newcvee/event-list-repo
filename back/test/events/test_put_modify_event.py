from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def xxtest_put_method_should_modify_event():
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

    body = {
        "id": "event-1",
        "name": "concierto queen",
        "description": "un tributo a queen de la ostia",
        "date": "2022-01-25",
        "public": 1,
        "time": "22:00:00",
        "categories": [],  # estaba:  "category-1"
    }

    response = client.put(
        "/api/events/event-1", json=body, headers={"Authorization": "user-1"}
    )
    assert response.status_code == 200

    response_get = client.get("api/events/event-1", headers={"Authorization": "user-1"})

    assert response_get.json == {
        "id": "event-1",
        "user_id": "user-1",
        "name": "concierto queen",
        "description": "un tributo a queen de la ostia",
        "date": "2022-01-25",
        "public": 1,
        "time": "22:00:00",
        "categories": [],  # estaba: "category-1"
    }
