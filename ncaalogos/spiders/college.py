# -*- coding: utf-8 -*-
import scrapy, urllib2
from ncaalogos.items import Logo


class CollegeSpider(scrapy.Spider):
    name = "college"
    allowed_domains = ["sportslogos.net"]
    start_urls = (
        'http://www.sportslogos.net/leagues/list_by_category/14/American_Colleges_-_NCAA/logos/',
    )

    def parse(self, response):
        urls = response.xpath("//ul[@class='logoWall']")
        # follow logo lists urls
        for url in urls.xpath('.//li/a/@href').extract():
            yield scrapy.Request('http://www.sportslogos.net/'+url.strip(), callback=self.parse_logolist)
            
    def parse_logolist(self, response):
        logolist = response.xpath("//ul[@class='logoWall']")
        # follow logo url links
        for logo in logolist.xpath('.//a'):
            url = logo.xpath('.//@href').extract()[0]
            yield scrapy.Request('http://www.sportslogos.net/'+url.strip(), callback=self.parse_logos)
            
    def parse_logos(self, response):
        # get current url
        primarylogos = response.xpath("//ul[@class='logoWall']")[0]
        
        # get current logo
        currentlogo = primarylogos.xpath('.//a')[-1]
        currentlogourl = currentlogo.xpath('.//@href').extract()[0]
        
        # get thumbnail url and title
        thmbnlsrc = currentlogo.xpath('.//img/@src').extract()[0]
        thmbnltitle = currentlogo.xpath('.//img/@title').extract()[0]
        
        # download thumbnail logo
        f = urllib2.urlopen(thmbnlsrc)
        data = f.read()
        with open(thmbnltitle + thmbnlsrc[-4:], "wb") as code:
            # write logo file to project folder
            code.write(data)
        
        # go to main logo page to get full-size log
        yield scrapy.Request('http://www.sportslogos.net/'+currentlogourl.strip(), callback=self.download_logo)
        
    def download_logo(self, response):
        # get main logo url and name
        mainLogoUrl = response.xpath("//div[@id='mainLogo']/img/@src").extract()[0]
        mainLogoTitle = response.xpath("//div[@id='mainLogo']/img/@title").extract()[0]
        
        # download main logo
        f = urllib2.urlopen(mainLogoUrl)
        data = f.read()
        with open(mainLogoTitle + mainLogoUrl[-4:], "wb") as code:
            # write logo file to project folder
            code.write(data)
            
