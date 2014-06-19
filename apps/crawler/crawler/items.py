# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from apps.search.models import Article

class ArticleItem(DjangoItem):
    # define the fields for your item here like:
    # name = Field()
    django_model = Article
