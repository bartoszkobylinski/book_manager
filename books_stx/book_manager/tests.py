from django.test import TestCase, Client
from django.urls import reverse
from book_manager.models import Book
from book_manager.forms import BookForm
from django.core.exceptions import ValidationError
from book_manager.languages import get_language_codes
from book_manager.google_book_api import GoogleAPIParser
from book_manager.CONSTANS import GOOGLE_API_KEY


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestDjangoInstallation(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_if_django_is_instaled_and_runs(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000")
        browser = driver
        self.assertIn("Django books", browser.title)


class TestBookModel(TestCase):

    def setUp(self):
        self.form = BookForm(data={
            'authors': "Jhon Doe",
            'title': "Django Cook Book",
            'publish_year': 1994,
            'isbn_13': "1234567890153",
            'pages': 1254,
            'cover': 'http://www.camy.pl',
            'language': 'pl'
        })

    def test_retrieving_and_saving_book_model(self):
        Book.objects.create(
            authors='Author',
            title="Title",
            publish_year=1520,
            isbn_13='12345678023',
            pages=152,
            cover='http:/eueu',
            language="pl")
        books_query = Book.objects.all()
        self.assertEqual(books_query.count(), 1)

    def test_assert_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            book = Book(
                authors='Author',
                title="Title",
                publish_year=1520,
                isbn_13='1234567890',
                pages=152,
                cover='http:/eueu',
                language="pl")
            book.full_clean()

    def test_book_form_is_valid_with_correct_data(self):
        self.form 
        self.assertTrue(self.form.is_valid())

    def test_book_form_is_not_valid_with_wrong_data(self):
        form = BookForm(data={
            'authors': "Jhon Doe",
            'title': "Django Cook Book",
            'publish_year': 1254,
            'isbn_13': "1234567890vvvvvvvvvvvvvvvv153",
            'pages': 1254,
            'cover': 'http://www.camy.pl',
            'language': 'pl'
        })
        self.assertFalse(form.is_valid())


class TestBookListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('books'))

    def test_book_list_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_book_list_view_is_using_correct_template(self):
        self.assertTemplateUsed(self.response, 'book_manager/books.html')


class TestAddBookView(TestCase):

    def setUp(self):
        self.client = Client()
        self.add_book_url = reverse('add_book')
        self.response = self.client.get(self.add_book_url)

    def test_response_add_book_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_add_book_view_is_using_correct_template(self):
        self.assertTemplateUsed(self.response, 'book_manager/add_book.html')

    def test_add_book_view_POST_method(self):

        self.client.post(
            self.add_book_url, {
                'authors': "Jhon Doe",
                'title': "Django Cook Book",
                'publish_year': 1965,
                'isbn_13': "1234567890123",
                'pages': 123123,
                'cover': 'http://www.camy.pl',
                'language': 'pl'})
        self.assertEqual(Book.objects.last().title, "Django Cook Book")


class TestLanguagesCode(TestCase):

    def test_if_get_language_codes(self):
        language_codes = get_language_codes()
        self.assertIsInstance(language_codes, list)

    def test_if_first_element_is_removed(self):
        language_codes = get_language_codes()
        self.assertNotIn("", language_codes)


class TestGoogleAPIParser(TestCase):

    def setUp(self):
        user_keywords = {
            'author': 'Robin Healey',
            'title': 'Italian Literature since 1900 in English Translation 1929-2016',
            'isbn': '9781487502928'
        }
        self.google_parser = GoogleAPIParser(GOOGLE_API_KEY, **user_keywords)

    def test_instantiation_google_parser(self):
        self.assertEqual(self.google_parser.title, 'Italian Literature since 1900 in English Translation 1929-2016')
        self.assertEqual(self.google_parser.google_key, GOOGLE_API_KEY)
        self.assertEqual(self.google_parser.isbn, '9781487502928')

    def test_string_method_for_google_parser(self):
        self.assertEqual(self.google_parser.__str__(), f'Google API parser for website: {GOOGLE_API_KEY}')

    def test_create_query_for_google_parser_with_isbn(self):
        self.assertEqual(
            self.google_parser.create_query(),
            f"{GOOGLE_API_KEY}{self.google_parser.author}+intitle:{self.google_parser.title}+isbn:{self.google_parser.isbn}"
            )

    def test_get_query_for_google_parser(self):
        self.assertEqual(self.google_parser.get_query()['totalItems'], 1)
        self.assertIsInstance(self.google_parser.get_query(), dict)
        self.assertEqual(list(self.google_parser.get_query().keys()), ['kind', 'totalItems', 'items'])

    def test_get_query_elements_for_google_parser(self):
        self.assertEqual(len(self.google_parser.get_query_elements()), 1)
        self.assertEqual(list(
            self.google_parser.get_query_elements()[0].keys()),
            ['kind', 'id', 'etag', 'selfLink', 'volumeInfo', 'saleInfo', 'accessInfo', 'searchInfo'])
        self.assertIsInstance(self.google_parser.get_query_elements()[0], dict)

    def test_get_keywords_for_google_parser(self):
        for element in self.google_parser.get_query_elements():
            autor = self.google_parser.get_authors(element)
            title = self.google_parser.get_title(element)
            isbn_13 = self.google_parser.get_isbn_13(element)
            isbn_10 = self.google_parser.get_isbn_10(element)
            pages = self.google_parser.get_pages(element)
            language = self.google_parser.get_language(element)
            cover_link = self.google_parser.get_cover_link(element)
            self.assertEqual(autor, 'Robin Healey')
            self.assertEqual(title, 'Italian Literature since 1900 in English Translation 1929-2016')
            self.assertEqual(isbn_13, "9781487502928")
            self.assertEqual(isbn_10, '1487502923')
            self.assertEqual(pages, 1104)
            self.assertEqual(language, 'en')
            self.assertEqual(cover_link[:37], 'http://books.google.com/books/content')
