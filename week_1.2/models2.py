import json

class db():
    def __init__(self, path):
        self.data = []
        self.path = path

    def load_item(self, item):
        self.load_data()
        self.data.append(item)
        self.upload_data()

    def load_data(self):
        with open(self.path) as file:
            self.data = json.load(file)
    
    def upload_data(self):
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)
    
    def return_id(self):
        self.load_data()
        if len(self.data) >= 1:
            last_task = self.data[-1]
            last_id = last_task.get("id") 
            return last_id + 1
        else:
            return 1

class task():
    def __init__(self, id, tittle, description, status):
        self.id = id
        self.tittle = tittle
        self.description = description
        self.status = status
    
    def to_dict(self):
        return {
            "id": self.id,
            "tittle": self.tittle,
            "description": self.description,
            "status": self.status
        }