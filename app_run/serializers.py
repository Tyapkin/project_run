from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from app_run.models import Run


class RunSerializer(ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'first_name', 'last_name']
