from django.test import LiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright

class TestCommonPages(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.playwright = sync_playwright().__enter__()
        cls.browser = cls.playwright.chromium.launch(headless=False)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.__exit__()
        super().tearDownClass()

    def setUp(self):
        self.page = self.browser.new_page()

    def tearDown(self):
        self.page.close()

    # def test_index_page_have_header(self):
    #     self.page.goto(f'{self.live_server_url}{reverse("index")}')
    #     header = self.page.locator('header')
    #     self.assertTrue(header, True)

