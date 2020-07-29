from main import Banner, BannerStore


class TestBanner:
    url = 'localhost/banner1.jpg'
    shows = 10
    category1 = 'category1'
    category2 = 'category2'
    categories = [category1, category2]

    def setup(self):
        self.banner = Banner(TestBanner.url, TestBanner.shows, TestBanner.categories)

    def test_init(self):
        assert self.banner.url == TestBanner.url
        assert self.banner.shows == TestBanner.shows
        assert self.banner.categories == TestBanner.categories

    def test_str(self):
        assert f'{self.banner.url}: {self.banner.shows}' == str(self.banner)

    def test_show(self):
        assert self.banner.show() == TestBanner.shows - 1
        assert self.banner.show() == TestBanner.shows - 2


class TestBannerStore:
    def setup(self):
        self.bs = BannerStore('test_fixtures/config.csv')

    def test_read_config(self):
        assert len(self.bs.store) == 7

    def test_put_banner(self):
        self.bs.put_banner(Banner('http://banners.com/banner3.jpg', 5, ['new category']))
        assert len(self.bs.store) == 8
        self.bs.put_banner(Banner('http://banners.com/banner4.jpg', 5, ['new category']))
        assert len(self.bs.store) == 8

    def test_remove_banner(self):
        banner = Banner('http://banners.com/banner3.jpg', 5, ['new category'])
        self.bs.put_banner(banner)
        self.bs.remove_banner(banner)
        assert self.bs.store['new category'] == []

    def test_remove_empty_categories(self):
        banner = Banner('http://banners.com/banner3.jpg', 5, ['new category'])
        self.bs.put_banner(banner)
        self.bs.remove_banner(banner)
        assert len(self.bs.store) == 8
        self.bs.remove_empty_categories(banner.categories)
        assert len(self.bs.store) == 7

    def test_is_category_empty(self):
        banner = Banner('http://banners.com/banner3.jpg', 5, ['new category'])
        self.bs.put_banner(banner)
        assert not self.bs.is_category_empty(banner.categories[0])
        self.bs.remove_banner(banner)
        assert self.bs.is_category_empty(banner.categories[0])

    def test_get_banner_by_category(self):
        banner = Banner('http://banners.com/banner3.jpg', 5, ['new category'])
        self.bs.put_banner(banner)
        assert self.bs.get_banner_by_category(banner.categories[0]) is banner

    def test_get_banner(self):
        assert isinstance(self.bs.get_banner(), Banner)
        assert isinstance(self.bs.get_banner(['new category']), Banner)
