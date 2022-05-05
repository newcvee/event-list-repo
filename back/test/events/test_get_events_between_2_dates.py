from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.events import EventsRepository, Event


def test_should_return_event_filtered_by_date():

    events_repository = EventsRepository(temp_file())
    app = create_app(repositories={"event": events_repository})
    client = app.test_client()

    concierto_camela = Event(
        id="event-2",
        user_id="user-1",
        name="concierto Camela",
        description="un tributo a camela",
        date="2020-03-25",
        public=1,
        time="20:00:00",
        categories=["category-1"],
    )
    concierto_joseba = Event(
        id="event-3",
        user_id="user-1",
        name="concierto joseba",
        description="un tributo a joseba el guitarrista",
        date="2022-04-28",
        public=1,
        time="20:00:00",
        categories=["category-1"],
    )
    josu_toca_la_flauta = Event(
        id="event-1",
        user_id="user-1",
        name="concierto josu",
        description="un tributo a josu el flautista",
        date="2023-02-28",
        public=0,
        time="20:00:00",
        categories=["category-2"],
    )
    events_repository.save(concierto_camela, "user-1")
    events_repository.save(concierto_joseba, "user-1")
    events_repository.save(josu_toca_la_flauta, "user-1")

    response = client.get(
        "/api/events/eventsbetween/2022-03-24/2022-05-25",
        headers={"Authorization": "user-1"},
    )

    assert response.status_code == 200
    event_filtered_response = response.json
    assert event_filtered_response[0]["id"] == "event-3"
    assert event_filtered_response[0]["user_id"] == "user-1"
    assert event_filtered_response[0]["name"] == "concierto joseba"
    assert event_filtered_response[0]["categories"] == []


def test_get_between_two_dates_if_user_wrong():

    events_repository = EventsRepository(temp_file())
    app = create_app(repositories={"event": events_repository})
    client = app.test_client()

    concierto_camela = Event(
        id="event-2",
        user_id="user-1",
        name="concierto Camela",
        description="un tributo a camela",
        date="2020-03-25",
        public=1,
        time="20:00:00",
        categories=["category-1"],
    )
    concierto_pakito = Event(
        id="event-3",
        user_id="user-1",
        name="concierto pakito",
        description="un tributo a pakito el guitarrista",
        date="2022-04-28",
        public=1,
        time="20:00:00",
        categories=["category-1"],
    )
    manolo_toca_la_flauta = Event(
        id="event-1",
        user_id="user-1",
        name="concierto manolo",
        description="un tributo a manolo el flautista",
        date="2023-02-28",
        public=0,
        time="20:00:00",
        categories=["category-2"],
    )
    events_repository.save(concierto_camela, "user-1")
    events_repository.save(concierto_pakito, "user-1")
    events_repository.save(manolo_toca_la_flauta, "user-1")
    response = client.get(
        "/api/events/eventsbetween/2022-03-24/2022-05-25",
        headers={"Authorization": "user-2"},
    )
    assert response.status_code == 200
    assert response.json == []


def test_shouldnt_return_nothing_if_dates_wrong_format():

    events_repository = EventsRepository(temp_file())
    app = create_app(repositories={"event": events_repository})
    client = app.test_client()

    concierto_camela = Event(
        id="event-2",
        user_id="user-1",
        name="concierto Camela",
        description="un tributo a camela",
        date="2020-03-25",
        public=1,
        time="20:00:00",
        categories=["category-1"],
    )
    concierto_pakito = Event(
        id="event-3",
        user_id="user-1",
        name="concierto pakito",
        description="un tributo a pakito el guitarrista",
        date="2022-04-28",
        public=1,
        time="20:00:00",
        categories=["category-1"],
    )
    manolo_toca_la_flauta = Event(
        id="event-1",
        user_id="user-1",
        name="concierto manolo",
        description="un tributo a manolo el flautista",
        date="2023-02-28",
        public=0,
        time="20:00:00",
        categories=["category-2"],
    )
    events_repository.save(concierto_camela, "user-1")
    events_repository.save(concierto_pakito, "user-1")
    events_repository.save(manolo_toca_la_flauta, "user-1")

    response = client.get(
        "/api/events/eventsbetween/03-2022-24/05-2022-25",
        headers={"Authorization": "user-1"},
    )
    assert response.status_code == 404
    assert response.data == b""
