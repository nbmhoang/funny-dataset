import scrapy


class XsmbSpider(scrapy.Spider):
    name = 'xsmb'
    # allowed_domains = ['http://hdmediagroup.vn/thongke2sotheotuan.html']
    # start_urls = ['http://http://hdmediagroup.vn/thongke2sotheotuan.html/']

    def start_requests(self):
        base_url = 'http://hdmediagroup.vn/thongke2sotheotuan.html'
        start = 2000
        end = 2020
        for year in range(start, end+1):
            yield scrapy.FormRequest(base_url, formdata={'form_block_id': '49786', 'from_year': str(year), 'sbtFind': 'Xem kết quả'}, callback=self.parse, meta={'year': str(year)})

    def parse(self, response):
        current_year = response.meta.get('year')
        l = response.css('div[title*="'+current_year+'"]')
        self.logger.info(current_year, len(l))
        for result in l:
            date = result.css('::attr(title)').get()
            text = result.css('::text').get().strip()
            if text:
                try:
                    s = int(text)
                    yield {
                        'date': date[:2],
                        'num': s
                    }
                except ValueError:
                    continue