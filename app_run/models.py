from django.db import models


class Run(models.Model):
    athlete = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Run by {self.athlete.username} on {self.created_at.date()}"
