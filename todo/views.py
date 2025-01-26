from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from todo.models import Task
from todo.serializers import TaskSerializer


# Create your views here.
class TaskViewSet(ModelViewSet):  # CRUD
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
