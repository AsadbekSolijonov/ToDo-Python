from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from todo.models import Task, Category
from todo.serializers import TaskSerializer, CategorySerializer


# Create your views here.
class TaskViewSet(ModelViewSet):  # CRUD
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['GET', 'PATCH'])
    def edit_status_true(self, request, pk=None):
        if request.method == 'PATCH':
            obj = self.get_object()
            obj.status = True
            obj.save()
            return Response({"message": "Task muvaffaqiyatli bajarildi!"}, status=status.HTTP_200_OK)

        if request.method == 'GET':
            return Response({"message": "Taskni bajarildi qilish uchun PATCH so'rov yuboring!"},
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET', 'PATCH'])
    def edit_status_false(self, request, pk=None):
        if request.method == 'PATCH':
            obj = self.get_object()
            obj.status = False
            obj.save()
            return Response({"message": "Task muvaffaqiyatli bajarilmadiga o'tkazildi!"}, status=status.HTTP_200_OK)

        if request.method == 'GET':
            return Response({"message": "Taskni bajarilmadi qilish uchun PATCH so'rov yuboring!"},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=['PATCH'], url_path='bulk-tasks-done', url_name='bulk-tasks-done')
    def bulk_tasks_done(self, request, *args, **kwargs):
        task_ids = request.data.get("task_ids")
        task_status = request.data.get('status')

        # validators
        if task_ids is None:
            return Response({"task_ids": ["This field is required"]})

        if task_status is None:
            return Response({"status": ["This field is required"]})

        if not task_ids:
            return Response({"task_ids": ["This field is not empty"]})

        if not isinstance(task_status, bool):
            return Response({"status": ["This field need to boolean field"]})

        tasks = Task.objects.filter(id__in=task_ids).update(status=task_status)
        return Response({"message": f"{tasks} tasks are updated succesfully!"}, status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def home(request):
    return render(request, 'index.html')
