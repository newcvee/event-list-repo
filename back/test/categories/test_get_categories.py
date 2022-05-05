from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.events import Event, EventsRepository
from src.domain.categories import CategoryRepository, Category


def test_delete_method_should_delete_event_by_id():

    categories_repository = CategoryRepository(temp_file())
    app = create_app(repositories={"categories": categories_repository})
    client = app.test_client()

    categoria_1 = Category(category_id="category-1", category_name="Cine")
    categoria_2 = Category(category_id="category-2", category_name="Partidos")
    categoria_3 = Category(category_id="category-3", category_name="Conciertos")
    categoria_4 = Category(category_id="category-4", category_name="Teatro")
    categoria_5 = Category(category_id="category-5", category_name="Conferencias")

    categories_repository.save(categoria_1)
    categories_repository.save(categoria_2)
    categories_repository.save(categoria_3)
    categories_repository.save(categoria_4)
    categories_repository.save(categoria_5)

    response = client.get("/api/categories")

    response.json == [
        {
            "category_id": "category-1",
            "category_name": "Cine",
        },
        {
            "category_id": "category-2",
            "category_name": "Partidos",
        },
        {
            "category_id": "category-3",
            "category_name": "Conciertos",
        },
        {
            "category_id": "category-4",
            "category_name": "Teatro",
        },
        {
            "category_id": "category-5",
            "category_name": "Conferencias",
        },
    ]


def test_should_save_catgeories_in_database():
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
        "categories": ["category-1", "category-2", "category-3"],
    }

    client.post("/api/events", json=body, headers={"Authorization": "user-1"})

    client.delete