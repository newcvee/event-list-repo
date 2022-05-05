from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def test_should_return_event_by_date():

    events_repository = EventsRepository(temp_file())
    app = create_app(repositories={"event": events_repository})
    client = app.test_client()

    concierto_queen = Event(
        id="event-1",
        user_id="user-1",
        name="concierto queen",
        description="un tributo a queen",
        date="2022-05-25",
        public=0,
        time="22:00:00",
        categories=["category-1"],
    )

    concierto_camela = Event(
        id="event-2",
        user_id="user-1",
        name="concierto Camela",
        description="un tributo a camela",
        date="2022-05-25",
        public=0,
        time="20:00:00",
        categories=["category-1"],
    )
    concierto_joseba = Event(
        id="event-3",
        user_id="user-1",
        name="concierto Camela",
        description="un tributo a camela",
        date="2022-05-28",
        public=0,
        time="20:00:00",
        categories=["category-1"],
    )
    events_repository.save(concierto_queen, "user-1")
    events_repository.save(concierto_camela, "user-1")
    events_repository.save(concierto_joseba, "user-1")

    response = client.get("/api/orderedevents", headers={"Authorization": "user-1"})

    assert response.status_code == 200
    ordered_events = response.json
    assert ordered_events[0]["user_id"] == "user-1"
    assert ordered_events[1]["user_id"] == "user-1"
    assert ordered_events[2]["user_id"] == "user-1"

    assert ordered_events[0]["id"] == "event-2"
    assert ordered_events[1]["id"] == "event-1"
    assert ordered_events[2]["id"] == "event-3"

    assert ordered_events[0]["name"] == "concierto Camela"
    assert ordered_events[1]["name"] == "concierto queen"
    assert ordered_events[2]["name"] == "concierto Camela"

    assert ordered_events[0]["categories"] == []
    assert ordered_events[1]["categories"] == []
    assert ordered_events[2]["categories"] == []
    # las tres son  "category-1"

    # assert response.json == [
    #     {
    #         "id": "event-2",
    #         "user_id": "user-1",
    #         "name": "concierto Camela",
    #         "description": "un tributo a camela",
    #         "date": "2022-05-25",
    #         "public": 0,
    #         "time": "20:00:00",
    #         "categories": [],
    #     },
    #     {
    #         "id": "event-1",
    #         "user_id": "user-1",
    #         "name": "concierto queen",
    #         "description": "un tributo a queen",
    #         "date": "2022-05-25",
    #         "public": 0,
    #         "time": "22:00:00",
    #         "categories": [],
    #     },
    #     {
    #         "id": "event-3",
    #         "user_id": "user-1",
    #         "name": "concierto Camela",
    #         "description": "un tributo a camela",
    #         "date": "2022-05-28",
    #         "public": 0,
    #         "time": "20:00:00",
    #         "categories": [],
    #     },
    # ]
