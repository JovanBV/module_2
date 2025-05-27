from abc import ABC, abstractmethod

class RepositoryManager(ABC):
    def __init__(self, db_manager):
        print("initializing repo manager")
        self.valid_car_condition = ['new', 'excellent', 'good', 'fair', 'poor', 'damaged', 'totaled', 'under_inspection', 'needs_repair']
        self.valid_account_status = ['active', 'inactive', 'suspended', 'pending', 'deleted', 'banned', 'locked', 'verified', 'unverified', 'archived']
        self.db_manager = db_manager

    def empty_table(self):
        try:
            query = f"delete from lyfter_car_rental.{self.table_name}"
            self.db_manager.cursor.execute(query)
        except:
            self.db_manager.connection.rollback()
            print("Error emptying table.")
            raise

    def get_all(self):
        try:
            query = f"SELECT * FROM lyfter_car_rental.{self.table_name}"
            self.db_manager.cursor.execute(query,)
            data = self.db_manager.cursor.fetchall()
            json_data = self.to_dict(data)
            return json_data
        except Exception as error:
            print("Error getting all entrys: ", error)

    def to_dict(self, data):
        return [self.return_json(entry) for entry in data]

    def return_json(self, data):
        if data:
            return dict(zip(self.valid_columns, data))
    
    def sort(self, sort_by, value):
        try:
            if sort_by not in self.valid_columns:
                raise ValueError("Query parameter not valid.")
            else:
                query = f"SELECT * FROM lyfter_car_rental.{self.table_name} WHERE {sort_by} = %s;"
                self.db_manager.cursor.execute(query, (value,))
                data = self.db_manager.cursor.fetchall()
                json_data = self.to_dict(data)
                return json_data
        except Exception as error:
            print(f"Error sorting by query parameter '{sort_by}' with value '{value}': ", error)
            return ({"error": f"{error}"})

    def get_by_id(self, id):
        try:
            query = f"""
            SELECT * FROM lyfter_car_rental.{self.table_name}
            WHERE id = %s;"""
            self.db_manager.cursor.execute(query, (id,))
            row = self.return_json(self.db_manager.cursor.fetchone())
            return row
        except Exception as error:
            return ({"error": f"{error}"})

    @abstractmethod
    def add_entry(self, *args):
        pass

    def update_with_id(self, id, new_value, column, valid_values):
        try:
            if new_value not in valid_values:
                raise ValueError("Condition is not valid")
            query = f"""
                UPDATE lyfter_car_rental.{self.table_name}
                SET {column} = %s 
                WHERE id = %s RETURNING id;"""
            self.db_manager.cursor.execute(query, (new_value, id))
            last_entry = self.db_manager.cursor.fetchone()
            self.db_manager.connection.commit()
            return last_entry
        except ValueError as ve:
            return {"error": str(ve)}
        except Exception as error:
            print("Error changing car condition: ", error)
            return None
