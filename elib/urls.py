from django.urls import path
from elib import views
from django.contrib import admin

urlpatterns = [
    path('', views.HomeElibView.as_view(), name='elib_index'),
    path('book/<int:book_id>/', views.BookDetail.as_view(), name='book_detail_by_id'),
    path('book/<slug:book_slug>/', views.BookDetail.as_view(), name='book_detail_by_slug'),
    path('books/<slug:genre_slug>/', views.BooksGenre.as_view(), name='books_by_genre'),
    path('books/', views.BooksList.as_view(), name='book_search'),
    path('add_book/', views.AddBook.as_view(), name='add_book'),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Мероприятия библиотеки"