import scrapy


class EmployeeSpider(scrapy.Spider):
    name = 'employee'
    allowed_domains = ['http://vku.udn.vn/doi-ngu']
    start_urls = ['http://vku.udn.vn/doi-ngu/']
    url = start_urls[0]

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        avatar = response.css('.about-img > img::attr(src)').extract()
        fullname = response.css('.about-text > span > h4::text').getall()

        # self.logger.info(len(names))
        for ava, name in zip(avatar, fullname):
            yield {
                'avatar_url': self.url + '/'.join(ava.replace('\r\n\t\t\t\t', '').split('/')[1:]),
                'name': name
            }