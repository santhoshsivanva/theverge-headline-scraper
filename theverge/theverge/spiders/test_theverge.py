import unittest
from scrapy.http import TextResponse
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from theverge_spider import TheVergeSpider


class TestTheVergeSpider(unittest.TestCase):

    def setUp(self):
        self.spider = TheVergeSpider()
        self.settings = get_project_settings()
        self.response = TextResponse(
            url='https://www.theverge.com/',
            request=None,
            headers={'Content-Type': 'text/html'},
        )

    def test_find_DMY(self):
        csv_name = self.spider.find_DMY()
        self.assertTrue(csv_name.endswith('_verge.csv'))

    def test_insert_headerSection(self):
        items = list(self.spider.insert_headerSection(self.response))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['URL'], 'https://www.theverge.com/features/2023/3/29/22353472/nextdoor-neighborhood-watch-app')
        self.assertEqual(items[0]['headline'], 'Nextdoor was supposed to make neighbors closer. It made them paranoid instead.')
        self.assertEqual(items[0]['author'], 'Kate Cox')
        self.assertEqual(items[0]['date'], 'Mar 29, 2023, 9:00am EDT')

    def test_insert_sideSection(self):
        items = list(self.spider.insert_sideSection(self.response))
        self.assertEqual(len(items), 5)
        self.assertEqual(items[0]['URL'], 'https://www.theverge.com/2023/3/29/22352502/nextdoor-neighborhood-watch-app-report')
        self.assertEqual(items[0]['headline'], 'Nextdoor was supposed to make neighbors closer. It made them paranoid instead.')
        self.assertEqual(items[0]['author'], 'Kate Cox')
        self.assertEqual(items[0]['date'], 'Mar 29, 2023, 9:00am EDT')

    def test_insert_mainSection(self):
        items = list(self.spider.insert_mainSection(self.response))
        self.assertEqual(len(items), 30)
        self.assertEqual(items[0]['URL'], 'https://www.theverge.com/features/2023/3/29/22353472/nextdoor-neighborhood-watch-app')
        self.assertEqual(items[0]['headline'], 'Nextdoor was supposed to make neighbors closer. It made them paranoid instead.')
        self.assertEqual(items[0]['author'], 'Kate Cox')
        self.assertEqual(items[0]['date'], 'Mar 29, 2023, 9:00am EDT')


if __name__ == '__main__':
    unittest.main()
