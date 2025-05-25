class RentalPopulator():
    def __init__(self, json_manager, repository):
        self.json_manager = json_manager
        self.repository = repository

    def populate_table(self):
        info = self.json_manager.load_data()
        for entry in info:
            self.repository.add_entry(
                entry['car_id'],
                entry['user_id'], 
                entry['rent_status']
            )
        print("Table CarUser populated succesfully!")