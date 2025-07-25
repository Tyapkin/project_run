"""
URL configuration for project_run project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app_run.views import AthleteInfoAPIView, ChallengeViewSet, RunStartAPIView, RunStopAPIView, RunViewSet, \
    UserViewSet, company_details

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'runs', RunViewSet, basename='run')
router.register(r'challenges', ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', company_details),
    path('api/', include(router.urls)),
    path('api/runs/<int:pk>/start/', RunStartAPIView.as_view()),
    path('api/runs/<int:pk>/stop/', RunStopAPIView.as_view()),
    path('api/athlete_info/<int:pk>/', AthleteInfoAPIView.as_view()),
]