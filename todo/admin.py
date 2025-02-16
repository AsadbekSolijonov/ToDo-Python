from django.contrib import admin

from todo.models import Task, Category, CustomUser, Profile

# Register your models here.
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Profile)
