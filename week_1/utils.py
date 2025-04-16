from flask import jsonify

def validate_status_value(request):
    valid_status = ['Pending', 'In progress', 'Completed']
    request_value = request.json["status"]
    if request_value not in valid_status:
        return jsonify(message= "Status is not valid, must be Pending, In progress or Completed")