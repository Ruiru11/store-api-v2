import psycopg2
import os
from app.models.tables import commands
from app import bcrypt
import uuid
from app.config import config_by_name


class Database_connection():
    def __init__(self):
        try:
            environment = os.getenv('ENV')
            database_url = configuration[environment].DATABASE_URL
            print('>>>>>>', database_url)
            self.connection = psycopg2.connect(database_url)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print("CANNOT CONNECT TO DATABASE INVALID DATABASE URL", error)

    def create_tables(self):
        for command in commands:
            self.cursor.execute(command)

    def create_admin(self):
        user_id = uuid.uuid4()
        encrypted_password = bcrypt.generate_password_hash(
            'adminpassword', 12).decode("utf-8")
        self.cursor.execute("""INSERT INTO users(id, email, password, role)
        VALUES(%s,%s,%s, %s);""",
                            (str(user_id), 'admin@mail.com', encrypted_password, 'admin'))
