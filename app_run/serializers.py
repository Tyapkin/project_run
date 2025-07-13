from django.contrib.auth.models import User

from rest_framework import serializers

from app_run.models import Run, AthleteInfo

class RunUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = RunUserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'first_name', 'last_name', 'type', 'runs_finished']

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        return 'athlete'

    def get_runs_finished(self, obj):
        return obj.run_set.filter(status=Run.RunStatus.FINISHED).count()


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(source='user_id')

    class Meta:
        model = AthleteInfo
        fields = ['goals', 'weight', 'user_id']

    def get_user_id(self, obj):
        return obj.user.id
