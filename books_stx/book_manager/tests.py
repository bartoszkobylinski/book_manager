from django.test import TestCase

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestDjangoInstallation(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_if_django_is_instaled_and_runs(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000")
        browser = driver
        self.assertIn("Django", browser.title)
