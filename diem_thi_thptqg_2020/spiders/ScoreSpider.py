import scrapy

class ScoreSpider(scrapy.Spider):
    name = "Scoreboard"

    def start_requests(self):
        base_url = 'http://diemthi.hcm.edu.vn/Home/Show'
        start_id = 2000001
        end_id = 2074719
        # end_id = 2000010
        for student_id in range(start_id, end_id+1):
            yield scrapy.FormRequest(url=base_url, formdata={'SoBaoDanh': '0{}'.format(student_id)}, callback=self.parse)

    def parse(self, response):
        for res in response.css('table > tr:nth-child(2) > td::text').getall():
            data = {
                'Toán': None,
                'Ngữ văn': None,
                'Vật lí': None,
                'Hóa học': None,
                'Sinh học': None,
                'KHTN': None,
                'KHXH': None,
                'Địa lí': None,
                'Lịch sử': None,
                'GDCD': None,
                'Tiếng Anh': None,
                # 'Tiếng Nhật': None,
                # 'Tiếng Nga': None,
                # 'Tiếng Pháp': None,
            }
            raw_text = res.strip()
            l = raw_text.split('   ')
            i = 0
            while i < len(l) - 1:
                subject_name = l[i][:-1]
                # self.logger.info(data.get(subject_name, None))
                if subject_name not in data.keys():
                    # self.logger.info('Unknown subject', subject_name)
                    if l[i][:4] in ('KHTN', 'KHXH'):
                        sub_name = l[i].split(' ')[0][:-1]
                        score = l[i].split(' ')[1]
                        data[sub_name] = score
                    i += 1
                else:
                    data[subject_name] = l[i+1]
                    i += 2
            if not all(score is None for score in data.values()):
                yield data
            else:
                self.logger.warn('Id not found')