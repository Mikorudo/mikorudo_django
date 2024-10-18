from django.urls import path, register_converter
from elib import views
from elib import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='elib_index'),
    path('books_by_year/<year4:year>/', views.books_by_year, name='books_by_year'),
    path('book_by_id/<int:id>/', views.book_by_id, name='book_by_id'),
    path('book_by_title/<str:title>/', views.book_by_title, name='book_by_title'),
]