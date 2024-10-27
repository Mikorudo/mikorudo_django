from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.db.models.functions import Length
from unidecode import unidecode


from elib.models import Books, Genres


def index(request):
    return redirect('book_search', permanent=True)


def book_by_id(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    return render(request, 'elib/book.html', {'book': book})


def book_by_slug(request, book_slug):
    book = get_object_or_404(Books, slug=book_slug)
    return render(request, 'elib/book.html', {'book': book})


def books_by_genre(request, genre_slug):
    books = Books.objects.filter(genres__slug=genre_slug).annotate(description_lengh = Length('short_description'))
    latest_book = Books.objects.latest('created_at')
    return render(request, 'elib/book_list.html', {'books': books, 'latest_book': latest_book})


def search_books(request):
    year = request.GET.get('year')
    title = request.GET.get('title')
    author = request.GET.get('author')
    genre_slug = request.GET.get('genre_slug')

    books = Books.objects.all()

    if title:
        books = books.filter(title__icontains=title)

    if author:
        books = books.filter(author__icontains=author)

    if genre_slug:
        books = books.filter(genres__slug=genre_slug)

    if year:
        books = books.filter(publication_year=year)

    books = books.annotate(description_length = Length('short_description'))
    latest_book = Books.objects.latest('created_at')
    return render(request, 'elib/book_list.html', {'books': books, 'latest_book': latest_book})


def create_book(title, author, publication_year, short_description, isbn, page_count, genre):
    slug = slugify(unidecode(f"{title} {author}"))

    unique_slug = slug
    counter = 1
    while Books.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    book = Books.objects.create(
        title=title,
        author=author,
        publication_year=publication_year,
        short_description=short_description,
        isbn=isbn,
        page_count=page_count,
        genre=genre,
        slug=unique_slug
    )
    return book

def update_book(book_id, **kwargs):
    book = get_object_or_404(Books, pk=book_id)

    for key, value in kwargs.items():
        if hasattr(book, key):
            setattr(book, key, value)

    if 'title' in kwargs or 'author' in kwargs:
        title = kwargs.get('title', book.title)
        author = kwargs.get('author', book.author)
        slug = slugify(unidecode(f"{title} {author}"))

        unique_slug = slug
        counter = 1
        while Books.objects.filter(slug=unique_slug).exclude(id=book_id).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        book.slug = unique_slug

    book.save()
    return book

def delete_book(book_id):
    book = get_object_or_404(Books, pk=book_id)
    book.delete()