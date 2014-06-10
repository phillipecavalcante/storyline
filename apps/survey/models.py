from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):

    N = 'N' # Neither/Other

    M = 'M' # Male
    F = 'F' # Female
    
    H = 'H' # High School
    U = 'U' # Undergraduate degree
    G = 'G' # Master's or doctoral degree
    
    GENDER_CHOICES = (
        (N, 'Neither/Other'),
        (M, 'Male'),
        (F, 'Female'),
    )
    
    EDU_CHOICES = (
        (N, 'Neither/Other'),
        (H, 'High School'),
        (U, 'Undergraduate'),
        (G, 'Graduate'),
    )
    
    user = models.OneToOneField(User)
    
    agreed = models.BooleanField(default=False)

    gender = models.CharField(
                            max_length=1,
                            choices=GENDER_CHOICES,
                            default=N
                            )
    edu = models.CharField(
                            max_length=1,
                            choices=EDU_CHOICES,
                            default=N
                            )
