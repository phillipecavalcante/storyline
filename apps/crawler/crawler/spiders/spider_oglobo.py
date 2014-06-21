import re
from datetime import datetime
from scrapy.contrib.spiders.crawl import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from crawler.items import ArticleItem


# REGEX
DOT = '\.'
SLASH = '/'
YEAR = '201[1-4]'
MONTH = '[0-3]\d'
YEAR_MONTH = YEAR + SLASH + MONTH + SLASH
ANY_CHAR_DIGIT = '[\w\d]+'
ANY_CHAR_DIGIT_HYPHEN = '[\d\-\w]+'

# OGLOBO SPIDER INFO
OGLOBO_SPIDER_NAME = 'oglobo'
OGLOBO_DOMAIN = 'oglobo.globo.com'
OGLOBO_START_URLS = [
                    'http://oglobo.globo.com/brasil',
                    ]

OGLOBO_URL_PATTERN = ANY_CHAR_DIGIT_HYPHEN

OGLOBO_ARTICLE_TITLE = '//h1/text()'
OGLOBO_ARTICLE_PUB_DATE = "//*[contains(@class, 'data-cadastro')]/time/@datetime"
OGLOBO_ARTICLE_CONTENT = "//*[contains(@itemprop, 'articleBody')]/p"

class OGLOBOSpider(CrawlSpider):
    
    name = OGLOBO_SPIDER_NAME
    allowed_domains = [ OGLOBO_DOMAIN ]
    start_urls = OGLOBO_START_URLS 

    rules = [
             Rule(SgmlLinkExtractor(
                                    allow=(OGLOBO_URL_PATTERN),
                                    ),
                                    callback='parse_item',
                                    follow=True,
                  ),
             ]

    
    def parse_item(self, response):
        
        sel = Selector(response)
        
        article = ArticleItem()
        
        article['source'] = 'O Globo'
        
        article['url'] = response.url
        
        title = sel.xpath(OGLOBO_ARTICLE_TITLE).extract()
        article['title'] = title[0] if title else None
        
        pub_date = sel.xpath(OGLOBO_ARTICLE_PUB_DATE).extract()
        pub_date = pub_date[0].replace('T', ' ')

        article['pub_date'] = datetime.strptime(pub_date, "%Y-%m-%d %H:%M")
        
        content = ' '.join(sel.xpath(OGLOBO_ARTICLE_CONTENT).extract())
        article['body'] = content if content else None 
        
        
        links = sel.xpath('//article//a/@href').extract()
        links = list(set(links))
        try:
            links.remove('javascript:;')
        except Exception:
            pass
        article['links'] = links
        
        return article