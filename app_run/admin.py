from django.contrib import admin

from app_run.models import AthleteInfo, Challenge, Run


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'created_at', 'comment')
    list_filter = ('status',)


@admin.register(AthleteInfo)
class AthleteInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'goals', 'weight')


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'full_name')
