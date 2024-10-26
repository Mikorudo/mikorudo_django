from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from unidecode import unidecode
from django.core.exceptions import ValidationError


from elib.models import Books

def index(request):
    return redirect('book_search', permanent=True)

def get_book_by_id(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    return render(request, 'elib/book.html', {'book': book})

def get_book_by_slug(request, book_slug):
    book = get_object_or_404(Books, slug=book_slug)
    return render(request, 'elib/book.html', {'book': book})

def search_books(request):
    year = request.GET.get('year')
    title = request.GET.get('title')
    author = request.GET.get('author')
    genre = request.GET.get('genre')

    books = Books.objects.all()

    if title:
        books = books.filter(title__icontains=title)

    if author:
        books = books.filter(author__icontains=author)

    if genre:
        books = books.filter(genre=genre)

    if year:
        books = books.filter(publication_year=year)

    return render(request, 'elib/book_list.html', {'books': books})

def create_book(title, author, publication_year, short_description, isbn, page_count, genre):
    if genre not in Books.Genre.values:
        raise ValidationError(f"Категория '{genre}' не существует")
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

    if 'genre' in kwargs and kwargs['genre'] not in Books.Genre.values:
        raise ValidationError(f"Жанр '{kwargs['genre']}' не существует")

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