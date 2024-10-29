import re
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Books, ISBN, Genres, UploadFiles


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789 - "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел"

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message,
                                  code=self.code, params={"value": value})

class AddBookForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=255)
    author = forms.CharField(label='Автор', max_length=255)
    publication_year = forms.IntegerField(label='Год публикации', min_value=1, max_value=datetime.now().year)
    short_description = forms.CharField(label='Краткое описание', widget=forms.Textarea, required=False, validators=[RussianValidator()])
    isbn = forms.CharField(label='ISBN', validators=[MinLengthValidator(10)])
    page_count = forms.IntegerField(label='Количество страниц', min_value=1)
    genres = forms.ModelMultipleChoiceField(label='Жанры', queryset=Genres.objects.all(), required=False)
    uploadedImg = forms.ModelChoiceField(label='Картинка', queryset=UploadFiles.objects.all(), required=False)


    def clean_isbn(self):
        isbn_str = self.cleaned_data['isbn']
        isbn_number = isbn_str.replace('-', '')

        if not re.fullmatch(r'\d{10}|\d{13}', isbn_number):
            raise ValidationError("ISBN должен содержать 10 или 13 цифр.")

        isbn_obj, created = ISBN.objects.get_or_create(isbn_number=isbn_number)
        return isbn_obj