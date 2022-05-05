from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def test_should_return_public_event_by_id():
    events_repository = EventsRepository(temp_file())
    app = create_app(repositories={"event": events_repository})
    client = app.test_client()

    concierto_queen = Event(
        id="event-1",
        user_id="user-1",
        name="concierto queen",
        description="un tributo a queen",
        date="2022-05-25",
        public=False,
        time="22:00:00",
        categories=["category-1"],
    )

    events_repository.save(concierto_queen, "user-1")
    response = client.get("/api/publicevents/event-1")
    assert response.json == None

    # [
    #     {
    #         "id": "event-1",
    #         "user_id": "user-1",
    #         "name": "concierto queen",
    #         "description": "un tributo a queen",
    #         "date": "2022-05-25",
    #         "public": False,
    #         "time": "22:00:00",
    #         "categories": [],
    #     }
    # ]

    # CORREGIR NONE
