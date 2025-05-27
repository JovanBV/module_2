from models.repo_manager import RepositoryManager


class UserRepository(RepositoryManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self._create_users_table()
        self.valid_columns = ['id', 'name', 'email', 'user_name', 'password', 'birth_date', 'account_status']
        self.valid_account_status = ['active', 'inactive', 'suspended', 'pending', 'deleted', 'banned', 'locked', 'verified', 'unverified', 'archived']
        self.table_name = 'users'

    def add_entry(self, *args):
        try:
            user_name = args[2]
            check_query = f"SELECT id FROM lyfter_car_rental.{self.table_name} WHERE user_name = %s"
            self.db_manager.cursor.execute(check_query, (user_name,))
            existing_user = self.db_manager.cursor.fetchone()

            if existing_user:
                raise

            query = f"""INSERT INTO lyfter_car_rental.{self.table_name} 
            (name, email, user_name, password, birth_date, account_status)
            VALUES(%s, %s, %s, %s, %s, %s)
            RETURNING id;"""

            self.db_manager.cursor.execute(query, args)
            last_entry = self.db_manager.cursor.fetchone()
            self.db_manager.connection.commit()
            return last_entry
        except Exception as error:
            print("Error inserting values into users database: ", error)
            raise

    def _create_users_table(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS lyfter_car_rental.users(
                id integer primary key generated always as identity, 
                name varchar(45) NOT NULL, 
                email varchar(45) NOT NULL, 
                user_name VARCHAR(45) NOT NULL UNIQUE, 
                password VARCHAR(45) NOT NULL, 
                birth_date DATE NOT NULL, 
                account_status VARCHAR(45) NOT NULL);"""
            self.db_manager.cursor.execute(query)
            print("Table 'users' created.")
        except Exception as error:
            print("Error creating the users table: ", error)
            self.db_manager.connection.rollback()
            raise
