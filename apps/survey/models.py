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
    
    AGE_CHOICES = (
        (N, 'Neither/Other'),
        ('ONE', '14 to 18'),
        ('TWO', '19 to 23'),
        ('THR', '24 to 28'),
        ('FOU', '29 to 33'),
        ('FIV', '34 to 38'),
        ('SIX', '39 to 43'),
        ('SEV', '44 to 48'),
        ('EIG', '49 to 53'),
        ('NIN', '54 to 58'),
        ('TEN', '59 or more'),
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

    age = models.CharField(
                            max_length=3,
                            choices=AGE_CHOICES,
                            default=N
                            )

class Ticket(models.Model):

    email = models.EmailField()
    token = models.CharField(max_length=255)


