# from crypt import methods
# from jinja2 import Undefined
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.domain.events import Event, EventsRepository
from src.domain.categories import Category, CategoryRepository
from src.lib.utils import object_to_json


def create_app(repositories):
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def hello_world():
        return "...magic!"

    # @app.route("/api/publicevents/<id>", methods=["GET"])
    # def get_public_events_by_id(id):
    #     print(id)
    #     public_event_by_id = repositories["event"].get_public_events_by_id(id)
    #     if public_event_by_id == None:
    #         return ("", 400)
    #     else:
    #         return object_to_json(public_event_by_id)

    @app.route("/api/events/publicevents", methods=["GET"])
    def public_events():
        all_events = repositories["event"].get_public_events()
        if all_events == None:
            return (None, 400)
        return object_to_json(all_events), 200

    @app.route("/api/events", methods=["GET"])
    def events_get_by_user_id():
        user_id = request.headers.get("Authorization")
        all_events = repositories["event"].search_by_user_id(user_id)
        return object_to_json(all_events), 200

    @app.route("/api/events", methods=["POST"])
    def events_save_by_user_id():
        user_id = request.headers.get("Authorization")
        data = request.json
        data["user_id"] = user_id
        event = Event(**data)
        event_id = data["id"]
        repositories["event"].save(event, user_id)
        repositories["category"].save_event_categories(event_id, data["categories"])
        if user_id == event.user_id:
            return ("", 200)
        else:
            return 403

    @app.route("/api/events/<id>", methods=["GET"])
    def events_get_by_id(id):
        user_id = request.headers.get("Authorization")
        event_by_id = repositories["event"].get_events_by_id(id, user_id)
        if event_by_id == None:
            return ("", 400)
        else:
            return object_to_json(event_by_id)

    @app.route("/api/events/<id>", methods=["DELETE"])
    def events_delete_by_id(id):
        user_id = request.headers.get("Authorization")
        asked_event = repositories["event"].get_events_by_id(id, user_id)
        print(asked_event)
        if user_id == asked_event.user_id:
            event_deleted = repositories["event"].delete_event_by_id(id, user_id)
            return ("", 200)
        else:
            return ("", 500)

    @app.route("/api/events/<id>", methods=["PUT"])
    def events_modify(id):
        user_id = request.headers.get("Authorization")
        data = request.json
        data["user_id"] = user_id
        event = Event(**data)
        repositories["event"].modify_event(id, event, user_id)
        if user_id == event.user_id:
            return ("", 200)
        else:
            return ("", 403)

    @app.route("/api/users", methods=["GET"])
    def users_get():
        all_users = repositories["user"].get_users()
        return object_to_json(all_users)

    # @app.route("/api/events/future/<date>", methods=["GET"])
    # def events_get_by_date(date):
    #     user_id = request.headers.get("Authorization")
    #     event_by_date = repositories["event"].get_future_events(date, user_id)
    #     return object_to_json(event_by_date), 200

    @app.route("/api/orderedevents", methods=["GET"])
    def events_get_by_date_ordered():
        user_id = request.headers.get("Authorization")
        all_events = repositories["event"].get_events_ordered_by_date(user_id)
        return object_to_json(all_events), 200

    @app.route("/api/monthlyevent/<date>", methods=["GET"])
    def get_last_month_events(date):

        user_id = request.headers.get("Authorization")
        monthly_events = repositories["event"].get_last_month_events(date, user_id)
        return object_to_json(monthly_events), 200

    @app.route("/api/events/eventsbetween/<datefrom>/<dateto>", methods=["GET"])
    def events_get_between_two_dates(datefrom, dateto):
        user_id = request.headers.get("Authorization")

        all_events = repositories["event"].get_events_between_two_dates(
            user_id, datefrom, dateto
        )
        if all_events == None:
            return ("", 404)
        else:
            return object_to_json(all_events), 200

    @app.route("/api/categories/<category_id>", methods=["GET"])
    def get_events_by_category(category_id):
        user_id = request.headers.get("Authorization")
        category_events = repositories["event"].get_events_by_categorie(
            category_id, user_id
        )
        if category_events == None:
            return ("", 404)
        else:
            return object_to_json(category_events), 200

    @app.route("/api/categories", methods=["GET"])
    def get_categories():
        categories = repositories["category"].get_categories()
        return object_to_json(categories)

    return app
