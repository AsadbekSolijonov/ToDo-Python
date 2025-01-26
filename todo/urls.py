from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todo.views import TaskViewSet, CategoryViewSet, home, csrf_view

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="tasks")
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path('home/', home, name="home"),
    path('csrf/', csrf_view, name='csrf'),
    path('', include(router.urls))
]
