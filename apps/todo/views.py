from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo, Task
from django.contrib.auth.models import User
import json
from base64 import b64decode
from django.contrib.auth import authenticate


class TodosView(View):

    def get(self, request: HttpRequest):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        todos = Todo.objects.filter(user=user)
        result = []
        for todo in todos:
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)
    
    def post(self,request: HttpRequest, user_id: int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        data= json.loads(request.body.decode())
        todo = Todo.objects.create(
            user=user,
            title=data.get('title'),
        )
        result=model_to_dict(todo)
        return JsonResponse(result, status=201)
    
    
class TodosItemView(View):

    def get(self, request: HttpRequest, todo_id:int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        result=model_to_dict(todo)
        return JsonResponse(result, safe=False)
    
    def put(self, request: HttpRequest, todo_id:int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        data=json.loads(request.body.decode())
        todo.user=user
        todo.title=data.get('title',todo.title)
        todo.save()
        result=model_to_dict(todo)
        return JsonResponse(result)
    
    def delete(self, request: HttpRequest, todo_id:int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        todo.delete()
        return JsonResponse({"message":"delete"})
        

class TasksView(View):
    def get(self, request: HttpRequest, todo_id: int) -> HttpRequest:
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        tasks = Task.objects.filter(todo=todo)

        result = []
        for task in tasks:
            result.append(model_to_dict(task))
        return JsonResponse(result, safe=False)
    
    def post(self,request: HttpRequest, todo_id: int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        data= json.loads(request.body.decode())
        task = Task.objects.create(
            todo=todo,
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            due_date=data.get('due_date'),
        )
        result=model_to_dict(task)
        return JsonResponse(result, status=201)
    

class TasksItemView(View):

    def get(self, request: HttpRequest, todo_id: int, task_id: int) -> HttpRequest:
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        try:
            task = Task.objects.get(id=task_id,todo=todo)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'task not found.'})
        result=model_to_dict(task)
        return JsonResponse(result, safe=False)
    
    def put(self, request: HttpRequest, todo_id:int, task_id:int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        todos = Todo.objects.filter(user=user)
        try:
            todo = Todo.objects.get(id=todo_id,user=user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        try:
            task = Task.objects.get(id=task_id,todo=todo)
        except User.DoesNotExist:
            return JsonResponse({'error': 'task not found.'})
        data=json.loads(request.body.decode())
        task.todo=todo
        task.title=data.get('title',task.title)
        task.description=data.get('description',task.description)
        task.status=data.get('status',task.status)
        task.due_date=data.get('due_date',task.due_date)
        task.save()
        result=model_to_dict(todo)
        return JsonResponse(result)
    
    def delete(self, request: HttpRequest, todo_id:int,task_id:int):
        header = request.headers
        token=header["Authorization"][6:]
        username,password=b64decode(token).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'error':'anauthorized'},status=401)
        todos = Todo.objects.filter(user=user)
        try:
            todo = Todo.objects.get(id=todo_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'todo not found.'})
        try:
            task = Task.objects.get(id=task_id,todo=todo)
        except User.DoesNotExist:
            return JsonResponse({'error': 'task not found.'})
        task.delete()
        return JsonResponse({"message":"delete"})