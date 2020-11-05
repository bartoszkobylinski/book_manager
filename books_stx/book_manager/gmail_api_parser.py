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
            query = f"{query}{self.author} "
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

    def get_books_from_query(self):
        books_query = self.get_query()
        books_list = []
        for book in books_query.get("items", ''):
            book_dict = {}
            authors = ''
            if len(book.get('volumeInfo', '').get('authors', '')) > 1:
                for author in book.get('volumeInfo', '').get('authors', ''):
                    authors += f"{author} "
                book_dict.update(authors=authors)
            else:
                book_dict.update(authors=book.get('volumeInfo', '').get('authors', '')[0])
            book_dict.update(title=book.get('volumeInfo', '').get('title', ''))
            book_dict.update(publish_year=book.get('volumeInfo', '').get('publishedDate', '')[:4])
            for isbn in book.get('volumeInfo', '').get('industryIdentifiers', ''):
                if isbn.get('type', '') == 'ISBN_13':
                    book_dict.update(isbn_13=isbn.get('identifier', ''))
                elif isbn.get('type', '') == 'ISBN_10':
                    book_dict.update(isbn_10=isbn.get('identifier', ''))
                elif isbn.get('type', '') == 'OTHER':
                    if isbn.get('identifier', '')[:4] == 'OCLC':
                        book_dict.update(oclc=isbn.get('identifier', ''))
                    elif isbn.get('identifier', '')[:4] == 'LCCN':
                        book_dict.update(lccn=isbn.get('identifier', ''))
            pages = book.get('volumeInfo', '').get('pageCount', '')
            if pages == '':
                book_dict.update(pages=0)
            else:
                book_dict.update(pages=pages)
            book_dict.update(language=book.get('volumeInfo', '').get('language', ''))
            if isinstance(book.get('volumeInfo', '').get('imageLinks', ''), str):
                book_dict.update(cover=book.get('volumeInfo', '').get('imageLinks', ''))
            else:
                book_dict.update(cover=book.get('volumeInfo', '').get('imageLinks', '').get('thumbnail', ''))
            books_list.append(book_dict)
        return books_list

    def save_books_to_database(self):
        books = self.get_books_from_query()
        print(books)
        Book.objects.bulk_create([Book(**book) for book in books])
