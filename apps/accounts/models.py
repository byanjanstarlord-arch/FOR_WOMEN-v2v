from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for HerSakhi."""
    # We can add additional fields here (e.g. current_year, career_goals, etc. from onboarding)
    dream_career = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username
