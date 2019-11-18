from crawler.crawling import Crawler


def test_get_links(test_html):
    expected_links = {
        'https://mac.test.com/',
        'https://mac.test.com/test.zip',
        'https://mac.test.com/download/test.dmg',
        'https://mac.test.com/download/test-1.0.0.tar.gz',
    }
    links = Crawler().get_links(html=test_html)
    assert links == expected_links
