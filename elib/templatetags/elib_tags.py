from django import template
from elib.models import Genres

register = template.Library()

@register.inclusion_tag('elib/books_genres.html')
def get_books_genres():
    books_genres = Genres.objects.all()
    return {'books_genres': books_genres}