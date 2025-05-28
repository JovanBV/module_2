
class UserPopulator():
    def __init__(self, json_manager, user_repository):
        self.json_manager = json_manager
        self.user_repository = user_repository

    def populate_users(self):
        users = self.json_manager.load_data()
        for user in users:
            self.user_repository.add_entry(
                user['name'],
                user['email'],
                user['user_name'],
                user['password'],
                user['birth_date'],
                user['account_state']
            )
        print("Table Users populated succesfully!")
        