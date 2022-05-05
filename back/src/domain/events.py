import sqlite3
from datetime import *

from src.domain.categories import Category, CategoryRepository
from src.domain.exports.date_validation import validation_2


database_path = "data/events-list.db"


class Event:
    def __init__(
        self, id, user_id, name, description, date, public, time, categories=None
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.date = date
        self.public = public
        self.time = time
        if not categories:
            categories = CategoryRepository(database_path).get_categories_by_event(id)
        self.categories = categories

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "public": self.public,
            "time": self.time,
            "categories": self.categories if self.categories else [],
        }


class EventsRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            create table if not exists events (
                id varchar PRIMARY KEY,
                user_id varchar,
                name text,
                description text,
                date text,
                public numeric,
                time text,
                categories text


                )
                """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def get_events(self):
        sql = """select * from events"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchall()
        result = []
        for item in data:
            event = Event(**item)
            result.append(event)
        conn.close()
        return result

    def search_by_user_id(self, user_id):
        sql = """select * from events WHERE user_id=:user_id ORDER BY date,time ASC"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"user_id": user_id})

        data = cursor.fetchall()
        result = []
        for item in data:
            event = Event(**item)

            result.append(event)
        conn.close()
        return result

    def get_events_by_id(self, id, user_id):
        sql = """select * from events where id=:id and user_id=:user_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": id, "user_id": user_id})
        event = cursor.fetchone()
        if dict(event):
            event = Event(**event)
        conn.close()
        return event

    # def get_public_events_by_id(self, id):
    #     sql = """SELECT * FROM events WHERE id=:id and public=true """
    #     conn = self.create_conn()
    #     cursor = conn.cursor()
    #     cursor.execute(sql, {"id": id})
    #     data = cursor.fetchone()
    #     print(data)
    #     event = data
    #     if event == None:
    #         return None
    #     else:
    #         event = Event(**data)
    #         return event

    def save(self, event, user_id):
        sql = """insert into events (id,user_id,name,description,date,public,time) values (
            :id, :user_id, :name, :description, :date, :public, :time)"""

        conn = self.create_conn()
        cursor = conn.cursor()
        params = event.to_dict()
        params["user_id"] = user_id
        cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return ""

    def delete_event_by_id(self, id, user_id):
        sql = """
            DELETE FROM events
            WHERE events.id = :id AND user_id=:user_id
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": id, "user_id": user_id})
        conn.commit()
        conn.close()
        return ""

    def modify_event(self, id, event, user_id):
        sql = """
            UPDATE events
            SET name= :name, description= :description,date= :date, time= :time, public = :public
            WHERE id = :id and user_id=:user_id
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        params = event.to_dict()
        params["user_id"] = user_id
        params["id"] = id
        cursor.execute(sql, params)
        conn.commit()
        conn.close()

    def get_future_events(self, date, user_id):

        sql = """select * from events where user_id=:user_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"user_id": user_id})

        data = cursor.fetchall()
        result = []
        for item in data:
            if item["date"] >= date:
                event = Event(**item)
                result.append(event)
        conn.close()
        return result

    def get_events_ordered_by_date(self, user_id):

        sql = """select * from events WHERE user_id=:user_id ORDER BY date,time ASC"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"user_id": user_id})

        data = cursor.fetchall()
        result = []
        current_day = str(datetime.today())
        for item in data:
            if item["date"] >= current_day[0:10]:
                event = Event(**item)
                result.append(event)
        conn.close()
        return result

    def get_last_month_events(self, date_from, user_id):
        sql = """
        SELECT * from events WHERE user_id=:user_id and date LIKE :date_from || '%'  ORDER BY date,time ASC"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"date_from": date_from, "user_id": user_id})
        data = cursor.fetchall()
        result = []
        for item in data:
            event = Event(**item)
            result.append(event)
        conn.close()
        return result

    def get_events_between_two_dates(self, user_id, datefrom, dateto):

        sql = """select * from events WHERE user_id=:user_id ORDER BY date,time ASC"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"user_id": user_id})
        data = cursor.fetchall()
        good_date = validation_2(datefrom, dateto)
        if good_date == None:
            conn.close()
            return None
        else:
            result = []
            for item in data:
                if item["date"] >= (datefrom) and item["date"] <= (dateto):
                    event = Event(**item)
                    result.append(event)
            conn.close()
            return result

    def get_events_by_categorie(self, events):
        event_id = events.id
        sql = """SELECT * FROM eventscategories
                 WHERE id = :id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": event_id})

        data = cursor.fetchall()
        categories = [i["category_id"] for i in data]
        conn.close()
        return categories

    def get_public_events(self):
        sql = """SELECT * from events WHERE public = 1"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        if data == None:
            return None
        result = []
        for item in data:
            event = Event(**item)
            result.append(event)
        return result
