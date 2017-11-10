import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor


class JobSpider(CrawlSpider):
    name = "jobs"
    auto_throttle_enabled = True
    download_delay = 1.5
    rules = (Rule(LinkExtractor(), callback="parse", follow=True),
             )

    base_url = 'https://www.indeed.com/jobs?q=Data+Scientist&start='

    start_urls = []

    page_num = 10

    for i in range(page_num):
        start_urls.append(base_url + str(10 * i))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in LinkExtractor(allow=r'\/rc\/').extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse_page)

    def parse_page(self, response):
        page = response.url.replace("/", "_")
        filename = 'jobs-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


if __name__ == "__main__":

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(JobSpider)
    process.start()