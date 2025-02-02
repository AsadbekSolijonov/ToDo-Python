from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todo.views import TaskViewSet, CategoryViewSet, home

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="tasks")
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path('home/', home, name="home"),
    path('', include(router.urls))
]
