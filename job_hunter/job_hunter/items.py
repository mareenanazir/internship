from scrapy import Item, Field


class JobHunterItem(Item):
    title = Field()
    job_url = Field()
    company_url = Field()
    date_posted = Field()
