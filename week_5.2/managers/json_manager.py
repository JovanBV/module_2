import json

class JsonManager():
    def __init__(self, path):
        self.path = path
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.path, 'r') as file:
                return json.load(file)
        except Exception as error:
            print("Error loading data from json: ", error)
