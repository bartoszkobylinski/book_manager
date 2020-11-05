from django.db import models
from django.urls import reverse


class Book(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    publish_year = models.DecimalField(max_digits=4, decimal_places=0)
    isbn = models.CharField(max_length=13)
    pages = models.PositiveIntegerField()
    cover = models.URLField()
    language = models.CharField(max_length=2)

    def get_absolute_url(self):
        return reverse('books')
