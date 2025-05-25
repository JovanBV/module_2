import psycopg2
from week_5.db_1 import PgManager
from week_5.repositories_1 import UserRepository


db_manager = PgManager(
    db_name="postgres", password="jovan", user="postgres", host="localhost",
)

users_repo = UserRepository(db_manager)
formatted_results = users_repo.get_all()


print(formatted_results)