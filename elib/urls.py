from django.urls import path
from elib import views

urlpatterns = [
    path('', views.index, name='elib_index'),
    path('book/<int:id>/', views.get_book, name='book_detail'),
    path('books/', views.search_books, name='book_search'),
]