import requests
import json
from book_manager.models import Book


class GmailAPIParser:

    def __init__(self, gmail_key, **kwargs):
        self.gmail_key = gmail_key
        self.author = kwargs.get('author', '')
        self.title = kwargs.get('title', '')
        self.isbn = kwargs.get('isbn', '')
        self.subject = kwargs.get('subject', '')
        self.publisher = kwargs.get('publisher', '')
        self.lccn = kwargs.get('lccn', '')
        self.oclc = kwargs.get('oclc', '')

    def __str__(self):
        return f"Gmail API parser for website: {self.gmail_key}"

    def create_query(self):
        query = self.gmail_key
        if self.author:
            query = f"{query}{self.author}"
        if self.title:
            query = f"{query}+intitle:{self.title}"
        if self.publisher:
            query = f"{query}+inpublisher:{self.publisher}"
        if self.subject:
            query = f"{query}+subject:{self.subject}"
        if not self.isbn:
            if self.oclc:
                query = f"{query}+oclc:{self.oclc}"
            if self.lccn:
                query = f"{query}+lccn:{self.lccn}"
        else:
            query = f"{query}+isbn:{self.isbn}"
        return query

    def get_query(self):
        query = self.create_query()
        if requests.get(query).status_code == 200:
            response = requests.get(query)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response

    def get_query_elements(self):
        query_elements = self.get_query()
        query_elements_list = query_elements.get("items", '')
        return query_elements_list

    def get_authors(self, query):
        authors = ''
        if len(query.get('volumeInfo', '').get('authors', '')) > 1:
            for author in query.get('volumeInfo', '').get('authors', ''):
                authors += f"{author} "
            return authors
        else:
            author = query.get('volumeInfo', '').get('authors', '')[0]
            return author

    def get_title(self, query):
        return query.get('volumeInfo', '').get('title', '')

    def get_isbn_13(self, query):
        for isbn_13 in query.get('volumeInfo', '').get('industryIdentifiers', ''):
            if isbn_13.get("type", "") == "ISBN_13":
                return isbn_13.get("identifier", "")

    def get_isbn_10(self, query):
        for isbn_10 in query.get('volumeInfo', '').get('industryIdentifiers', ''):
            if isbn_10.get("type", "") == "ISBN_10":
                return isbn_10.get("identifier", "")

    def get_oclc_number(self, query):
        for oclc_number in query.get('volumeInfo', '').get('industryIdentifiers', ''):
            if oclc_number.get('type', '') == 'OTHER':
                if oclc_number.get('identifier', '')[:4] == 'OCLC':
                    return oclc_number.get('identifier', '')

    def get_lccn_number(self, query):
        for lccn_number in query.get('volumeInfo', '').get('industryIdentifiers', ''):
            if lccn_number.get('type', '') == 'OTHER':
                if lccn_number.get('identifier', '')[:4] == 'OCLC':
                    return lccn_number.get('identifier', '')

    def get_pages(self, query):
        return query.get('volumeInfo', '').get('pageCount', '')

    def get_language(self, query):
        return query.get('volumeInfo', '').get('language', '')

    def get_cover_link(self, query):
        if isinstance(query.get('volumeInfo', '').get('imageLinks', ''), str):
            return query.get('volumeInfo', '').get('imageLinks', '')
        else:
            return query.get('volumeInfo', '').get('imageLinks', '').get('thumbnail', '')

    def get_books_from_query(self):
        books_list = []
        for element in self.get_query_elements():
            book = {}
            book.update(authors=self.get_authors(element))
            book.update(title=self.get_title(element))
            book.update(isbn_13=self.get_isbn_13(element))
            book.update(isbn_10=self.get_isbn_10(element))
            book.update(oclc_number=self.get_oclc_number(element))
            book.update(lccn_number=self.get_lccn_number(element))
            book.update(pages=self.get_pages(element))
            book.update(language=self.get_language(element))
            book.update(cover=self.get_cover_link(element))
            books_list.append(book)
        return books_list

    def save_books_to_database(self):
        books = self.get_books_from_query()
        print(books)
        Book.objects.bulk_create([Book(**book) for book in books])
