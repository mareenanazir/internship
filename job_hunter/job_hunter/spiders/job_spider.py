from datetime import datetime, timedelta

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import JobHunterItem


def get_job_date(time):
    time_period = time.split(' ')
    date_posted = datetime.now()
    if time_period[1] == 'hours' or time_period[1] == 'hour':
        date_posted - timedelta(hours=int(time_period[0]))
    elif time_period[1] == 'days' or time_period[1] == 'day':
        date_posted - timedelta(days=int(time_period[0]))

    return date_posted


def validate_time(time):
    time_period = time.split(' ')
    return True if ((time_period[1] == 'days' and int(time_period[0]) <= 30) or
                    time_period[1] == 'day' or time_period[1] == 'hours' or time_period[1] == 'hour') else False


class JobsSpider(CrawlSpider):
    name = 'job'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['https://news.ycombinator.com/jobs']
    rules = [
        Rule(LinkExtractor(restrict_css='[rel="next"] a'))
    ]

    def parse(self, response):
        titles = response.css('.storylink::text').getall()
        company_urls = response.css('.sitebit a::attr(href)').getall()
        job_urls = response.css('.storylink::attr(href)').getall()
        times_posted = response.css('.age a::text').getall()

        for i in range(len(company_urls)):
            item = JobHunterItem()
            item['title'] = titles[i]
            item['company_url'] = company_urls[i]
            item['job_url'] = job_urls[i]
            item['date_posted'] = times_posted[i]

            if validate_time(item['date_posted']):
                item['date_posted'] = get_job_date(item['date_posted'])
                yield item
            else:
                return
