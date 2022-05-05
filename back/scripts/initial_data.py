import sys

sys.path.insert(0, "")

import sqlite3

from src.domain.events import EventsRepository, Event
from src.domain.users import UsersRepository, User
from src.domain.categories import CategoryRepository, Category

database_path = "data/events-list.db"


concierto_queen = Event(
    id="event-1",
    user_id="user-1",
    name="concierto queen",
    description="un tributo a queen",
    date="2022-01-25",
    public=False,
    time="22:00",
    categories=["category-1"],
)

concierto_iker = Event(
    id="event-2",
    user_id="user-1",
    name="concierto iker",
    description="un tributo a iker",
    date="2022-01-26",
    public=False,
    time="23:00",
    categories=["category-1"],
)
concierto_camelia = Event(
    id="event-3",
    user_id="user_2",
    name="concierto camelia",
    description="un tributo a camelia",
    date="2022-01-27",
    public=False,
    time="21:00",
    categories=["category-1"],
)
concierto_ainara = Event(
    id="event-4",
    user_id="user-2",
    name="concierto ainara",
    description="un tributo a ainara",
    date="2022-01-28",
    public=False,
    time="17:00",
    categories=["category-2"],
)
concierto_valentina = Event(
    id="event-5",
    user_id="user-1",
    name="Valentina",
    description="un tributo a valentina",
    date="2022-04-09",
    public=False,
    time="22:00",
    categories=["category-2"],
)
concierto_ruth = Event(
    id="event-6",
    user_id="user-1",
    name="Ruth",
    description="un tributo a ruth",
    date="2022-04-15",
    public=False,
    time="22:00",
    categories=["category-2"],
)
concierto_jefferson = Event(
    id="event-7",
    user_id="user-1",
    name="Jeff the killer",
    description="un tributo a creppy jeff",
    date="2022-04-15",
    public=False,
    time="22:00",
    categories=["category-2"],
)


event_repository = EventsRepository(database_path)
event_repository.save(concierto_queen, "user-1")
event_repository.save(concierto_iker, "user-1")
event_repository.save(concierto_ainara, "user-2")
event_repository.save(concierto_camelia, "user-2")
event_repository.save(concierto_valentina, "user-1")
event_repository.save(concierto_ruth, "user-1")
event_repository.save(concierto_jefferson, "user-1")


user_ainara = User(
    id="user-1",
    user_name="Ainara",
)

user_camelia = User(
    id="user-2",
    user_name="Camelia",
)

user_repository = UsersRepository(database_path)
user_repository.save(user_ainara)
user_repository.save(user_camelia)

category_cine = Category(category_id="category-1", category_name="Cine")
category_partidos = Category(category_id="category-2", category_name="Partidos")
category_conciertos = Category(category_id="category-3", category_name="Conciertos")
category_teatro = Category(category_id="category-4", category_name="Teatro")
category_conferencias = Category(category_id="category-5", category_name="Conferencias")
category_festivales = Category(category_id="category-6", category_name="Festivales")
category_bbcs = Category(category_id="category-7", category_name="BBCs")
category_familiares = Category(
    category_id="category-8", category_name="eventos familiares"
)
category_repository = CategoryRepository(database_path)
category_repository.save(category_cine)
category_repository.save(category_partidos)
category_repository.save(category_conciertos)
category_repository.save(category_teatro)
category_repository.save(category_conferencias)
category_repository.save(category_festivales)
category_repository.save(category_bbcs)
category_repository.save(category_familiares)
