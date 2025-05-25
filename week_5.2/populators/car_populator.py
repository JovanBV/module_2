class CarPopulator():
    def __init__(self, car_repository, json_manager):
        self.car_repository = car_repository
        self.json_manager = json_manager


    def populate_cars(self):
        cars = self.json_manager.load_data()
        for car in cars:
            self.car_repository.add_entry(
                car['make'],
                car['model'],
                car['year'],
                car['condition']
            )
        print("Table Cars populated succesfully!")
