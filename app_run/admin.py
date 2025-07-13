from django.contrib import admin

from app_run.models import Run, AthleteInfo


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'created_at', 'comment')
    list_filter = ('status',)


@admin.register(AthleteInfo)
class AthleteInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'goals', 'weight')
