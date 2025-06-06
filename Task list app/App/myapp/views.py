import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token  

TASKS_FILE = "tasks.json"

def initialize_storage_file(file_path=TASKS_FILE):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_tasks_to_file(tasks, file_path=TASKS_FILE):
    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=4)

@csrf_exempt
def create_task(request):
    if request.method == "POST":
        tasks = initialize_storage_file() 

        try:
            data = json.loads(request.body)  
            title = data.get("title")
            description = data.get("description", "")
            status = data.get("status", "To do")
            due_date = data.get("due_date")

            if not title or len(title) < 5:
                return JsonResponse({"status": "error", "message": "Title must be at least 5 characters long."})

            task_id = max([task["id"] for task in tasks], default=0) + 1  

            task = {
                "id": task_id, 
                "title": title,
                "description": description,
                "status": status,
                "due_date": due_date,
            }

            tasks.append(task)
            save_tasks_to_file(tasks)

            return JsonResponse({"status": "success", "message": "Task created successfully.", "data": {"task": task}})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt
def get_tasks(request):
    tasks = initialize_storage_file()  
    return JsonResponse({"status": "success", "message": "Tasks retrieved successfully.", "data": tasks})

@csrf_exempt
def get_overdue_tasks(request):
    tasks = initialize_storage_file() 
    overdue_tasks = [task for task in tasks if task["due_date"] and task["due_date"] < str(now()) and task["status"] == "To do"]
    
    if not overdue_tasks:
        return JsonResponse({"status": "error", "message": "No overdue tasks found."})

    return JsonResponse({"status": "success", "message": "Overdue tasks retrieved successfully.", "data": overdue_tasks})

@csrf_exempt
def delete_task(request, task_id):
    tasks = initialize_storage_file()

    task_to_delete = next((task for task in tasks if task.get("id") == task_id), None)

    if task_to_delete:
        tasks.remove(task_to_delete)  
        save_tasks_to_file(tasks)  
        return JsonResponse({
            "status": "success",
            "message": f"Task with ID {task_id} deleted successfully."
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": f"Task with ID {task_id} not found."
        })

@csrf_exempt 
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password") 

            if not username or not password:
                return JsonResponse({"error": "Please provide both username and password"}, status=400)

            user = authenticate(request, username=username, password=password)
            
            if user:
                token, created = Token.objects.get_or_create(user=user) 
                return JsonResponse({"token": token.key})
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
