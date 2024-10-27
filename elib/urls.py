from django.urls import path
from elib import views

urlpatterns = [
    path('', views.index, name='elib_index'),
    path('book/<int:book_id>/', views.book_by_id, name='book_detail_by_id'),
    path('book/<slug:book_slug>/', views.book_by_slug, name='book_detail_by_slug'),
    path('books/<slug:genre_slug>/', views.books_by_genre, name='books_by_genre'),
    path('books/', views.search_books, name='book_search'),
]