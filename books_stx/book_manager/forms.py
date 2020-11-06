from django import forms
from book_manager.models import Book
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'authors',
            'title',
            'publish_year',
            'isbn_10',
            'isbn_13',
            'oclc_number',
            'lccn_number',
            'pages',
            'cover',
            'language',
            'subject']

    def clean_isbn(self):
        value = self.cleaned_data['isbn']
        if len(str(value)) != 10 and len(str(value)) != 13:
            raise ValidationError("Your ISBN number has not valid length")
        elif len(str(value)) == 13 and str(value).isnumeric() is False:
            raise ValidationError(
                "Your ISBN number should have 13 char. It should contain only numeric characters")
        elif len(str(value)) == 10 and str(value).isalnum() is False:
            raise ValidationError(
                "Your ISBN number should have 10 characters. It should contain only alphanumeric characters")
        return value


class GoogleApiForm(forms.Form):
    title = forms.CharField(required=False)
    authors = forms.CharField()
    publisher = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    isbn_number = forms.CharField(required=False)
    lccn_number = forms.CharField(required=False)
    oclc_number = forms.CharField(required=False)
