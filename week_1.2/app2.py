from flask import Flask, request, jsonify
from flask.views import MethodView
from models2 import task, db


app = Flask(__name__)

class TaskManager(MethodView):

    def get(self):
        data_base.load_data()

        if "status" in request.args:
            status = request.args.get("status")
            filtered_task = []
            for task in data_base.data:
                if task.get("status") == status:
                    filtered_task.append(task)
            return jsonify(filtered_task)
        else:
            return data_base.data
        
    def post(self):
        required_keys = {"tittle", "description", "status"}

        try:
            if not required_keys.issubset(request.json):
                raise ValueError(f'Key missing from the body')
        except ValueError as ex:
            return jsonify(message=str(ex)), 400

        validation = validate_status_value(request)
        if validation:
            return validation

        instance = task(
            data_base.return_id(), 
            request.json["tittle"], 
            request.json["description"],
            request.json["status"]
        )
        
        try:
            instance = instance.to_dict()
            data_base.load_item(instance)
            return data_base.data
        except:
            raise ValueError("Error with file or path")

    def delete(self, task_id):
        data_base.load_data()

        task_found = False
        for i, task in enumerate(data_base.data):
            if task.get("id") == task_id:
                deleted_task = data_base.data.pop(i)
                task_found = True
                break
        
        if not task_found:
            return jsonify(message= f'Task does not exist on database.')

        data_base.upload_data()
        return jsonify(message= f'Task with the id {task_id} has been eliminated.', task=deleted_task)

    def put(self, task_id):
        data_base.load_data()

        validation = validate_status_value(request)
        if validation:
            return validation

        task_found = False
        for i, task in enumerate(data_base.data):
            if task.get("id") == task_id:
                for key, value in request.json.items():
                    if key != "id":
                        data_base.data[i][key] = value
                task_found = True
                break
        
        if not task_found:
            return jsonify(message="Task Id not found in database"), 404
        
        try:
            data_base.upload_data()
        except:
            return jsonify(message=f"Error saving data"), 500

        return jsonify(data_base.data[i])


def validate_status_value(request):
    valid_status = ['Pending', 'In progress', 'Completed']
    request_value = request.json["status"]
    if request_value not in valid_status:
        return jsonify(message= "Status is not valid, must be Pending, In progress or Completed")
    return None

if __name__ == "__main__":
    path = "C:/Users/jovan/Documents/module_2/week_1.2//flask_exercise2.json"
    data_base = db(path)

    task_view = TaskManager.as_view('task')

    app.add_url_rule('/task', view_func=task_view, methods=["GET", "POST"])
    app.add_url_rule('/task/<int:task_id>', view_func=task_view, methods=["DELETE", "PUT"])

    app.run(host="localhost", debug=True)