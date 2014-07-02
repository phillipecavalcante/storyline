from django.db import models
from django.contrib.auth.models import User
from apps.search.models import Article

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
                            max_length=3,
                            choices=GENDER_CHOICES,
                            default=N
                            )
    edu = models.CharField(
                            max_length=3,
                            choices=EDU_CHOICES,
                            default=N
                            )

    age = models.CharField(
                            max_length=3,
                            choices=AGE_CHOICES,
                            default=N
                            )
    
    def is_filled(self):
        if self.edu != self.N and self.gender != self.N and self.age != self.N:
            return True
        return False
    
    def __unicode__(self):
        return self.user.username

class Ticket(models.Model):

    email = models.EmailField()
    token = models.CharField(max_length=255)


class Story(models.Model):

    first = models.ForeignKey(Article)
    users = models.ManyToManyField(User, through='UserStory')
    
    def first_story_id(self):
        return str(self.first.id)
    first_story_id.short_description = 'First Story ID'
    
    def __unicode__(self):
        return self.first.title


class StoryRank(models.Model):

    story = models.ForeignKey(Story)
    article = models.ForeignKey(Article)
    rank = models.IntegerField()

    def first_story_id(self):
        return str(self.story.first.id)
    first_story_id.short_description = 'First Story ID'
    
    def __unicode__(self):
        return str(self.story.first.id)

class UserStory(models.Model):
    N = 'N'
    YES = 'YES'
    NO = 'NO'
    
    BOOLEAN_CHOICES = (
        (N, 'Neither/Other'),
        (YES,'Yes'),
        (NO,'No')
    )
    
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story)
    
    # eval
    has_read = models.CharField(max_length=3,choices=BOOLEAN_CHOICES, default=N)
    has_context = models.CharField(max_length=3,choices=BOOLEAN_CHOICES, default=N)
    has_gap = models.CharField(max_length=3,choices=BOOLEAN_CHOICES, default=N)
    has_similar = models.CharField(max_length=3,choices=BOOLEAN_CHOICES, default=N)
    
    class Meta:
        unique_together = (('user', 'story'),)

    def __unicode__(self):
        return "%s : %s" % (self.user.username, self.story.first.title)

class UserStoryRank(models.Model):

    userstory = models.ForeignKey(UserStory)
    article = models.ForeignKey(Article)
    rank = models.IntegerField()

    def first_story_id(self):
        return str(self.userstory.story.first.id)
    first_story_id.short_description = 'First Story ID'
    
    def __unicode__(self):
        return str(self.userstory.story.first.id)
