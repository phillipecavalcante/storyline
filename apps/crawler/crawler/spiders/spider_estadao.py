# -*- coding: utf-8 -*-

## NAO FUNCIONA

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

# ESTADAO SPIDER INFO
ESTADAO_SPIDER_NAME = 'estadao'
ESTADAO_DOMAIN = 'http://politica.estadao.com.br'
ESTADAO_START_URLS = [
                    'http://politica.estadao.com.br/noticias/',
                    ]

ESTADAO_URL_PATTERN = ANY_CHAR_DIGIT_HYPHEN

ESTADAO_PODER = re.compile(ESTADAO_URL_PATTERN)
#ESTADAO_PODEREPOLITICA = re.compile('/poder/poderepolitica/' + ESTADAO_URL_PATTERN)


ESTADAO_ARTICLE_TITLE = '//*/article/header/h1/text()'
ESTADAO_ARTICLE_PUB_DATE = '//*/article/header/p[2]/text()'
ESTADAO_ARTICLE_CONTENT = '//*/article/p'

class EstadaoSpider(CrawlSpider):
    
    name = ESTADAO_SPIDER_NAME
    allowed_domains = [ ESTADAO_DOMAIN ]
    start_urls = ESTADAO_START_URLS 

    rules = [
             Rule(SgmlLinkExtractor(
                                    allow=(ESTADAO_PODER),
                                    ),
                                    callback='parse_item',
                                    follow=True,
                  ),
             ]

    
    def parse_item(self, response):
        
        sel = Selector(response)
        
        article = ArticleItem()
        
        article['source'] = 'O Estadão'
        
        article['url'] = response.url
        
        title = sel.xpath(ESTADAO_ARTICLE_TITLE).extract()
        article['title'] = title[0] if title else None
        
        pub_date = sel.xpath(ESTADAO_ARTICLE_PUB_DATE).extract()[0]

        article['pub_date'] = datetime.strptime(pub_date, "%Y-%m-%d %H:%M")
        
        content = ' '.join(sel.xpath(ESTADAO_ARTICLE_CONTENT).extract())
        article['body'] = content if content else None 
        
        
        links = sel.xpath('//article//a/@href').extract()
        links = list(set(links))
        try:
            links.remove('javascript:;')
        except Exception:
            pass
            
        article['links'] = links
        
        return article