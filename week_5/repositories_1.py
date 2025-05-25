class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def _format_user(self, user_record):
        return {
            "id": user_record[0],
            "full_name": user_record[1],
            "email": user_record[2],
            "password": user_record[3],
        }
    
    def get_all(self):
        try:
            results = self.db_manager.execute_query(
                "SELECT * FROM lyfter_duad.users;"
            )
            formatted_results = [self._format_user(result) for result in results]
            return formatted_results
        except Exception as error:
            print("Error getting all usert from the database: ", error)
            return False