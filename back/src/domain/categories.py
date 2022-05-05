import sqlite3


class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
        }


class CategoryRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql1 = """
            create table if not exists categories (
                category_id varchar PRIMARY KEY,
                category_name text
                );

            create table if not exists eventscategories (
                id VARCHAR,
                category_id VARCHAR,
                FOREIGN KEY (id) REFERENCES events(id),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
				
                )
          
            """

        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.executescript(sql1)
        conn.commit()
        conn.close()

    def get_categories(self):
        sql = """select * from categories """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        categories = [Category(**item) for item in data]
        conn.close()
        return categories

    def get_categories_by_event(self, event_id):
        conn = self.create_conn()
        cursor = conn.cursor()
        sql_categories = """select c.category_id, c.category_name 
            from eventscategories ec, categories c 
            where ec.category_id=c.category_id and id=:id"""
        cursor.execute(sql_categories, {"id": event_id})
        categories = cursor.fetchall()
        categories = [Category(**item).to_dict() for item in categories]
        conn.close()
        return categories

    def save(self, categories):
        sql = """insert into categories (category_id,category_name) values (:category_id, :category_name) """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, categories.to_dict())
        # self.save_event_categories(cursor, event_id, categories)
        conn.commit()
        conn.close()

    def get_events_categories(self, event_id):
        sql = """SELECT * FROM eventscategories
                 WHERE id = :id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": event_id})

        data = cursor.fetchall()
        categories = [i["category_id"] for i in data]

        return categories

    def save_event_categories(self, event_id, categories):
        sql = """
        DELETE FROM eventscategories WHERE id = :id
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(
            sql,
            {"id": event_id},
        )
        conn.commit()
        sql_event_categories = """INSERT INTO eventscategories (id, category_id) VALUES (:id, :category_id)"""

        for cat in categories:
            cursor.execute(sql_event_categories, {"id": event_id, "category_id": cat})
        conn.commit()
        conn.close()

    # def save_category_event(self, category):
    #     sql = """insert into eventscategories  (id,category_id) values (:id, :category_id) """
    #     conn = self.create_conn()
    #     cursor = conn.cursor()
    #     cursor.execute(sql, category.to_dict())
