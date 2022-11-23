import scrapy


class YatubeSpider(scrapy.Spider):
    name = 'yatube'
    allowed_domains = ['51.250.32.185']
    start_urls = ['http://51.250.32.185/']

    def parse(self, response):
        for post in response.css('div.card-body'):
            yield {
                'author': post.css('strong.d-block::text').get(),
                'text': ' '.join(
                    t.strip() for t in post.css('p.card-text::text').getall()
                ),
                'date': post.css('small.text-muted::text').get(),
            }

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
