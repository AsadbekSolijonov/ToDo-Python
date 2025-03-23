from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, \
    DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from todo.models import Task, Category, CustomUser, Profile
from todo.permissions import IsOwnerOrSuperUser, IsTaskOwnerOrSuperUser
from todo.serializers import TaskSerializer, CategorySerializer, CustomUserSerializer, ProfileSerializer, \
    RegisterUserSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class TaskViewSet(ModelViewSet):  # CRUD
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwnerOrSuperUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'category__name']
    ordering_fields = ['title', 'description', 'category__name']

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

    @action(detail=False, methods=['PATCH'])
    def change_status(self, request, *args, **kwargs):
        BOOL_STATUS = ['True', 'False']
        task_status = request.query_params.get('all_status')
        task_status = task_status.capitalize()
        if task_status in BOOL_STATUS:
            tasks = Task.objects.all().update(status=task_status)
            return Response({"message": f"{tasks} task status successfully updated!"}, status=status.HTTP_200_OK)
        return Response({'detail': "write bool status in params"}, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ModelViewSet):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    @method_decorator(cache_page(60))  # 1 minut
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):  # list, create, retrieve
        return super().dispatch(*args, **kwargs)

    # @method_decorator(cache_page(60 * 60 * 2))  # 2 soat kesh
    # @method_decorator(vary_on_cookie)
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(60 * 60 * 2))  # 2 soat kesh
    # @method_decorator(vary_on_cookie)
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # @method_decorator(cache_page(60 * 60 * 2))  # 2 soat kesh
    # @method_decorator(vary_on_cookie)
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)


class CostumUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    # permission_classes = [DjangoModelPermissions, ]
    # renderer_classes = [JSONRenderer, ]


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    # renderer_classes = [JSONRenderer, ]


class RegisterUserAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foydalanuvchi muvofaqqiyatli yaratildi!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'index.html')
