from django import forms
from datetime import date
from book_manager.models import Book
from django.core.validators import URLValidator


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

    def clean_isbn_13(self):
        value = self.cleaned_data['isbn_13']
        if len(str(value)) != 13:
            raise forms.ValidationError("Your ISBN number has not valid length. It should has 13 numbers")
        elif len(str(value)) == 13 and str(value).isnumeric() is False:
            raise forms.ValidationError(
                "Your ISBN number should have 13 char. It should contain only numeric characters without dashes")
        return value

    def clean_isbn_10(self):
        value = self.cleaned_data['isbn_10']
        if len(str(value)) != 10:
            raise forms.ValidationError("Your ISBN number has not valid length. It should has 10 numbers")
        elif len(str(value)) == 10 and str(value).isalnum() is False:
            raise forms.ValidationError(
                "Your ISBN number should have 10 char. It should contains only alphanumeric characters without dashes")

    def clean_publish_year(self):
        value = self.cleaned_data.get('publish_year', '')
        if value > date.today().year or value < 1900:
            raise forms.ValidationError(
                f"Publish year has to be beetwen 1900 and {date.today().year}. Your year is: {value}")


class GoogleApiForm(forms.Form):
    title = forms.CharField(required=False)
    authors = forms.CharField()
    publisher = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    isbn_number = forms.CharField(required=False)
    lccn_number = forms.CharField(required=False)
    oclc_number = forms.CharField(required=False)
