from django.db import models
from django.contrib.auth.models import User

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255)  # Google Place ID
    place_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} visiting {self.place_name} from {self.start_date} to {self.end_date}"