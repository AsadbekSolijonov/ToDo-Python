from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todo.views import TaskViewSet, CategoryViewSet, CostumUserViewSet, ProfileViewSet, home

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="tasks")
router.register("categories", CategoryViewSet, basename="categories")
router.register('users', CostumUserViewSet, basename='custom-users')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('home/', home, name="home"),
    path('', include(router.urls))
]
