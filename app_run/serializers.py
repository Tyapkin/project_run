from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_run.models import Run


class RunSerializer(ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(ModelSerializer):
    type = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'first_name', 'last_name', 'type']

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        return 'athlete'
