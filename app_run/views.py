from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from app_run.models import AthleteInfo, Challenge, Run
from app_run.serializers import AthleteInfoSerializer, ChallengeSerializer, RunSerializer, UserSerializer


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'


@api_view(['GET'])
def company_details(request):
    details = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS
    }
    return Response(details)


class RunViewSet(ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    search_fields = ['athlete__first_name', 'athlete__last_name']
    filterset_fields = ['status', 'athlete']
    pagination_class = CustomPagination


class UserViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for retrieving user information.
    
    This viewset provides 'list' and 'retrieve' actions for User objects,
    excluding superusers. It supports filtering by user type ('coach' or 'athlete')
    via query parameters.
    """
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser=False)
    lookup_field = 'is_staff'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['username', 'date_joined', 'first_name', 'last_name']
    pagination_class = CustomPagination
    
    def get_queryset(self) -> 'QuerySet[User]':
        """
        Filter the queryset based on the 'type' query parameter.

        Returns:
            QuerySet[User]: Filtered queryset of User objects.
                - If type='coach': returns staff users
                - If type='athlete': returns non-staff users
                - Otherwise: returns all non-superuser users
        """
        user_type = self.request.query_params.get('type')

        # Use a dictionary mapping for cleaner, more maintainable code
        type_filters = {
            'coach': {'is_staff': True},
            'athlete': {'is_staff': False}
        }

        if user_type in type_filters:
            return self.queryset.filter(**type_filters[user_type])

        return self.queryset


class RunStartAPIView(APIView):
    def post(self, request, pk, format=None):
        run = get_object_or_404(Run, pk=pk)
        if run.status not in [Run.RunStatus.IN_PROGRESS, Run.RunStatus.FINISHED]:
            serializer = RunSerializer(run, data={'status': Run.RunStatus.IN_PROGRESS}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Run already started'}, status=status.HTTP_400_BAD_REQUEST)


class RunStopAPIView(APIView):
    def create_challenge(self, athlete: User) -> None:
        if athlete.run_set.filter(status=Run.RunStatus.FINISHED).count() == 10:
            serializer = ChallengeSerializer(data={'athlete': athlete.id, 'full_name': 'Сделай 10 забегов'})
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    def post(self, request, pk, format=None):
        run = get_object_or_404(Run, pk=pk)
        if run.status == Run.RunStatus.IN_PROGRESS:
            serializer = RunSerializer(run, data={'status': Run.RunStatus.FINISHED}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.create_challenge(run.athlete)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Run not started'}, status=status.HTTP_400_BAD_REQUEST)


class AthleteInfoAPIView(APIView):
    def get(self, request, pk, format=None):
        athlete_info, created = AthleteInfo.objects.get_or_create(user=get_object_or_404(User, pk=pk))
        athlete_info = AthleteInfoSerializer(athlete_info, data=athlete_info.to_dict())
        if athlete_info.is_valid(raise_exception=True):
            return Response(athlete_info.data, status=status.HTTP_200_OK)
        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """Update athlete's info"""
        user = get_object_or_404(User, pk=pk)
        athlete_info, _ = AthleteInfo.objects.update_or_create(user=get_object_or_404(User, pk=pk))
        serializer = AthleteInfoSerializer(athlete_info, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChallengeViewSet(ModelViewSet):
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.select_related('athlete').all()

    def get(self, request, *args, **kwargs):
        challenge = get_object_or_404(Challenge, athlete_id=request.query_params.get('athlete'))
        serializer = ChallengeSerializer(challenge)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)