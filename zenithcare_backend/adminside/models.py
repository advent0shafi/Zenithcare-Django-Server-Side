from django.db import models
from authentification.models import User
# Create your models here.
class TherapistReport(models.Model):
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_reports')
    report_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"Report by {self.reported_by} on {self.report_date}"