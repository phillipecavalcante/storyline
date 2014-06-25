from django.contrib import admin

from apps.search.models import Topic, Article
# Register your models here.

class TopicAdmin(admin.ModelAdmin):

    list_display = ['name', 'terms']
    list_editable = ['terms']

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Article, ArticleAdmin)