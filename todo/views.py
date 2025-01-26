from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.viewsets import ModelViewSet

from todo.models import Task, Category
from todo.serializers import TaskSerializer, CategorySerializer


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class TaskViewSet(ModelViewSet):  # CRUD
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def home(request):
    return render(request, 'index.html')


@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({"message": "CSRF cookie set."})
