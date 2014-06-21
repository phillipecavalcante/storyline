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

# FOLHA SPIDER INFO
FOLHA_SPIDER_NAME = 'folha'
FOLHA_DOMAIN = 'www1.folha.uol.com.br'
FOLHA_START_URLS = [
                    'http://www1.folha.uol.com.br/poder',
#                   'http://www1.folha.uol.com.br/poder/poderepolitica'
                    ]

FOLHA_URL_PATTERN = YEAR_MONTH + ANY_CHAR_DIGIT_HYPHEN + DOT + ANY_CHAR_DIGIT

FOLHA_PODER = re.compile('/poder/' + FOLHA_URL_PATTERN) 
#FOLHA_PODEREPOLITICA = re.compile('/poder/poderepolitica/' + FOLHA_URL_PATTERN)


FOLHA_ARTICLE_TITLE = '//h1/text()'
FOLHA_ARTICLE_PUB_DATE = '//header/time/@datetime'
FOLHA_ARTICLE_CONTENT = '//article/div[@itemprop="articleBody"]/p [not(@class="wideVideoPlayer") and not(@class="star") and not(descendant::img)]'

class FolhaSpider(CrawlSpider):
    
    name = FOLHA_SPIDER_NAME
    allowed_domains = [ FOLHA_DOMAIN ]
    start_urls = FOLHA_START_URLS 

    rules = [
             Rule(SgmlLinkExtractor(
                                    allow=(FOLHA_PODER),
                                    ),
                                    callback='parse_item',
                                    follow=True,
                  ),
#             Rule(SgmlLinkExtractor(
#                                    allow=(FOLHA_PODEREPOLITICA),
#                                    ),
#                                    callback='parse_item',
#                                    follow=True,
#                  ),
             ]

    
    def parse_item(self, response):
        
        sel = Selector(response)
        
        article = ArticleItem()
        
        article['source'] = 'Folha de S.Paulo'
        
        article['url'] = response.url
        
        title = sel.xpath(FOLHA_ARTICLE_TITLE).extract()
        article['title'] = title[0] if title else None
        
        pub_date = sel.xpath(FOLHA_ARTICLE_PUB_DATE).extract()[0]
        print pub_date, " <<<<<<  aqui"

        article['pub_date'] = datetime.strptime(pub_date, "%Y-%m-%d %H:%M")
        
        content = ' '.join(sel.xpath(FOLHA_ARTICLE_CONTENT).extract())
        article['body'] = content if content else None 
        
        
        links = sel.xpath('//article//a/@href').extract()
        links = list(set(links))
        try:
            links.remove('javascript:;')
        except Exception:
            pass
            
        article['links'] = links
        
        return article