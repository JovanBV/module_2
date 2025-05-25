from models.repo_manager import RepositoryManager

class CarRepository(RepositoryManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.valid_columns = ['id', 'make', 'model', 'year', 'condition']
        self.table_name = "cars"
        self._create_cars_table()

    def _create_cars_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS lyfter_car_rental.cars(
            id integer primary key generated always as identity, 
            make VARCHAR(45) NOT NULL,
            model VARCHAR(45) NOT NULL,
            year VARCHAR(45) NOT NULL,
            condition VARCHAR(45) NOT NULL
            )"""
            self.db_manager.cursor.execute(query)
            print("Table 'cars' created.")
        except Exception as error:
            print("Error creating cars database: ", error)
            self.db_manager.connection.rollback()
            raise

    def add_entry(self, *args):
        try:

            car_condition = args[3]
            if not car_condition  in self.valid_car_condition:
                raise

            query = f"""INSERT INTO lyfter_car_rental.{self.table_name} (make, model, year, condition)VALUES(%s, %s, %s, %s) RETURNING id;"""
            self.db_manager.cursor.execute(query, args)
            last_entry = self.db_manager.cursor.fetchone()
            self.db_manager.connection.commit()
            return last_entry
        except Exception as error:
            print("Error inserting values into cars database: ", error)
            raise