from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from todo.models import Task, Category, CustomUser, Profile


# 3c8c2c92-a510-4a84-b63f-6c515ceaee61
class TaskSerializer(serializers.ModelSerializer):
    # category_name = SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'status']
        read_only_fields = ('id',)

    # def get_category_name(self, obj):
    #     return obj.category.name


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tasks', 'user']
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'bio', 'avatar', 'user')
        read_only_fields = ('id',)


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    # categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile', 'phone_number']
        read_only_fields = ('id',)


from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PhoneNumberAuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.check_password(password):
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("Telefon raqam yoki parol noto‘g‘ri.")


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'username', 'password', 'password2']
        extra_fields = {"phone_number": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            return serializers.ValidationError('parol yoki phone_number xato!')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return CustomUser.objects.create_user(**validated_data)
