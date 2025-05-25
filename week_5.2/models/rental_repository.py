from models.repo_manager import RepositoryManager


class RentalRepository(RepositoryManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.table_name = 'car_user'
        self.valid_columns = ['id', 'car_id', 'user_id', 'rent_status']
        self._create_table_car_user()


    def _create_table_car_user(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS lyfter_car_rental.car_user(
            id INTEGER PRIMARY key generated always as identity,
            car_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rent_status VARCHAR(45) NOT NULL,
            rent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (car_id) REFERENCES lyfter_car_rental.cars(id),
            FOREIGN KEY (user_id) REFERENCES lyfter_car_rental.users(id));"""
            self.db_manager.cursor.execute(query)
            print("Table 'car_user' created.")
        except Exception as error:
            print("Error creating the car_user table: ", error)
            self.db_manager.connection.rollback()
            raise 


    def add_entry(self, *args):
        try:
            query = f"""INSERT INTO lyfter_car_rental.{self.table_name} (car_id, user_id, rent_status)VALUES(%s, %s, %s) RETURNING id;"""
            self.db_manager.cursor.execute(query, args)
            last_entry = self.db_manager.cursor.fetchone()
            self.db_manager.connection.commit()
            return last_entry
        except Exception as error:
            print("Error inserting values into rental database: ", error)
            raise