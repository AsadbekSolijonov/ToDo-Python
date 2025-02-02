from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from todo.models import Task, Category
from todo.serializers import TaskSerializer, CategorySerializer


# Create your views here.
class TaskViewSet(ModelViewSet):  # CRUD
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def home(request):
    return render(request, 'index.html')
