from django.db import models
from django.urls import reverse
from django.core.validators import URLValidator


class Book(models.Model):
    authors = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=250, null=True)
    publish_year = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    isbn_10 = models.CharField(max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    oclc_number = models.CharField(max_length=25, blank=True, null=True)
    lccn_number = models.CharField(max_length=25, blank=True, null=True)
    pages = models.PositiveIntegerField(null=True)
    cover = models.URLField(blank=True, validators=[URLValidator])
    language = models.CharField(max_length=2, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('books')
