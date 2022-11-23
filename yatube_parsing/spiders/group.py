import scrapy


class GroupSpider(scrapy.Spider):
    name = 'group'
    allowed_domains = ['51.250.32.185']
    start_urls = ['http://51.250.32.185/']

    def parse(self, response):
        all_groups = response.css('a.group_link::attr(href)')
        for group_link in all_groups:
            return response.follow(group_link, callback=self.parse_group)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        group = response.css('div.card')
        yield {
            'group_name': group.css('h2::text').strip(),
            'description': group.css('p.group_descr::text'),
            'posts_count': int(
                ' '.join(t.strip() for t in group.css(
                    'div.posts_count::text').getall()).split()[1]
            ),
        }
