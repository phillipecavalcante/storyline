from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.survey.models import Profile, Story, StoryRank, UserStory, UserStoryRank
from apps.search.models import Article
from apps.engine.chaining import storyline

# Register your models here.

def make_user_story(modeladmin, request, queryset):
    for obj in queryset:
        stories = Story.objects.all()
        for story in stories:
            UserStory.objects.create(user=obj, story=story)
make_user_story.short_description = "User Storylines"

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    actions = [make_user_story]

def make_storyline(modeladmin, request, queryset):
    for obj in queryset:
        first_id = str(obj.first.id)
        for rank, art in enumerate(storyline(first_id)):
            storyrank = StoryRank(story=obj, rank=rank)
            doc_id = art['id']
            storyrank.article = Article.objects.get(pk=doc_id)
            storyrank.save()
make_storyline.short_description = "Storyline of selected articles"


class StoryAdmin(admin.ModelAdmin):
    list_display = ['first_story_id', 'first']
    search_fields = ['first']
    actions = [make_storyline]

class StoryRankAdmin(admin.ModelAdmin):
    search_fields = ['story', 'article']
    list_display = ['first_story_id', 'story', 'rank', 'article']


class UserStoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'story']

class UserStoryRankAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Story, StoryAdmin)
admin.site.register(StoryRank, StoryRankAdmin)
admin.site.register(UserStory, UserStoryAdmin)
admin.site.register(UserStoryRank, UserStoryRankAdmin)