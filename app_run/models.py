from django.db import models


class Run(models.Model):
    class RunStatus(models.TextChoices):
        INIT = 'init'
        IN_PROGRESS = 'in_progress'
        FINISHED = 'finished'

    athlete = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=11,
        choices=RunStatus,
        default=RunStatus.INIT
    )

    def __str__(self) -> str:
        return f"Run by {self.athlete.username} on {self.created_at.date()}"


class AthleteInfo(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    goals = models.TextField(blank=True)
    weight = models.FloatField(default=1, blank=True)

    def to_dict(self) -> dict:
        return {
            'user': self.user.id,
            'goals': self.goals,
            'weight': self.weight,
        }

