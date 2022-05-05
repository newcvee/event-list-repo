from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def test_get_method_should_return_this_month_events():
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
        user_id="user-1",
        name="concierto Camela",
        description="un tributo a camela",
        date="2022-01-15",
        public=0,
        time="23:00:00",
        categories=["category-1"],
    )

    events_repository.save(concierto_queen, "user-1")
    events_repository.save(concierto_camela, "user-1")

    response = client.get(
        "/api/monthlyevent/2022-01", headers={"Authorization": "user-1"}
    )
    assert response.status_code == 200
    response_month_events = response.json
    assert response_month_events[0]["user_id"] == "user-1"
    assert response_month_events[1]["user_id"] == "user-1"

    assert response_month_events[0]["id"] == "event-2"
    assert response_month_events[1]["id"] == "event-1"

    assert response_month_events[0]["date"] == "2022-01-15"
    assert response_month_events[1]["date"] == "2022-01-25"

    assert response_month_events[0]["categories"] == []
    assert response_month_events[1]["categories"] == []
    # todas son   "category-1"

    # assert response.json == [
    #     {
    #         "id": "event-2",
    #         "user_id": "user-1",
    #         "name": "concierto Camela",
    #         "description": "un tributo a camela",
    #         "date": "2022-01-15",
    #         "public": 0,
    #         "time": "23:00:00",
    #         "categories": [],
    #     },
    #     {
    #         "id": "event-1",
    #         "user_id": "user-1",
    #         "name": "concierto queen",
    #         "description": "un tributo a queen",
    #         "date": "2022-01-25",
    #         "public": 0,
    #         "time": "22:00:00",
    #         "categories": [],
    #     },
    # ]
