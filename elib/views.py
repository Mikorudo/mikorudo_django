from django.http import Http404
from django.shortcuts import render, redirect

# Заглушка пока нет БД
books = [
    {
        'id': 0,
        'title': 'Python Programming',
        'author': 'John Doe',
        'genres': ['Programming', 'Technology'],
        'publication_year': 2021,
        'short_description': 'A comprehensive guide to Python programming.',
        'isbn': '978-3-16-148410-0',
        'page_count': 350,
    },
    {
        'id': 1,
        'title': 'Django for Beginners',
        'author': 'Jane Smith',
        'genres': ['Web Development', 'Programming'],
        'publication_year': 2020,
        'short_description': 'Learn how to build web applications with Django.',
        'isbn': '978-1-59327-914-1',
        'page_count': 200,
    },
    {
        'id': 2,
        'title': 'Data Science with Python',
        'author': 'Alice Johnson',
        'genres': ['Data Science', 'Programming'],
        'publication_year': 2019,
        'short_description': 'An introduction to data science using Python.',
        'isbn': '978-1-49195-565-1',
        'page_count': 400,
    },
]

def index(request):
    return redirect('book_search', permanent=True)


def get_book(request, id):
    book = next((b for b in books if b['id'] == id), None)

    if book is None:
        raise Http404("Книга не найдена.")

    return render(request, 'elib/book.html', {'book': book})


def search_books(request):
    year = request.GET.get('year')
    title = request.GET.get('title')
    author = request.GET.get('author')
    genres = request.GET.getlist('genres')

    filtered_books = list(books)

    if title:
        filtered_books = [b for b in filtered_books if title.lower() in b['title'].lower()]

    if author:
        filtered_books = [b for b in filtered_books if author.lower() in b['author'].lower()]

    if genres:
        filtered_books = [b for b in filtered_books if any(genre in b['genres'] for genre in genres)]

    if year:
        filtered_books = [b for b in filtered_books if b['publication_year'] == year]

    return render(request, 'elib/book_list.html', {'books': filtered_books})