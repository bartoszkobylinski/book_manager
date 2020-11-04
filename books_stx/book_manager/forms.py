from django.forms import ModelForm
from book_manager.models import Book
from django.core.exceptions import ValidationError


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'title', 'publish_year', 'isbn', 'pages', 'cover', 'language']

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
