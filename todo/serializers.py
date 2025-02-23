from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from todo.models import Task, Category, CustomUser, Profile


class TaskSerializer(serializers.ModelSerializer):
    category_name = SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'status', 'category_name']
        read_only_fields = ('id',)

    def get_category_name(self, obj):
        return obj.category.name


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tasks']
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'bio', 'avatar', 'user')
        read_only_fields = ('id',)


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile', 'phone_number']
        read_only_fields = ('id',)
