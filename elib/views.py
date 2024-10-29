from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models.functions import Length
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from elib.forms import AddBookForm
from elib.models import Books

class HomeElibView(TemplateView):
    template_name = 'elib/book_search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Электронная библиотека'
        context['books'] = Books.objects.all().annotate(description_length = Length('short_description'))
        context['latest_book'] = Books.objects.latest('created_at')
        return context

class BooksList(ListView):
    model = Books
    template_name = 'elib/book_list.html'
    context_object_name = 'books'
    extra_context = {
        'title': 'Книги',
        'latest_book': Books.objects.latest('created_at'),
    }

class BooksGenre(ListView):
    template_name = 'elib/book_list.html'
    context_object_name = 'books'
    allow_empty = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Книги по категориям'
        context['latest_book'] = Books.objects.latest('created_at')
        return context
    def get_queryset(self):
        return Books.objects.all().filter(genres__slug=self.kwargs['genre_slug']).annotate(description_lengh = Length('short_description'))

class VIEW_AddBook(View):
    def get(self, request):
        form = AddBookForm()
        return render(request, 'elib/add_book.html', context={'form': form, 'title': 'Добавление новой книги'})

    def post(self, request):
        form = AddBookForm(request.POST)
        if form.is_valid():
            try:
                book = Books.objects.create(
                    title=form.cleaned_data['title'],
                    author=form.cleaned_data['author'],
                    publication_year=form.cleaned_data['publication_year'],
                    short_description=form.cleaned_data['short_description'],
                    isbn=form.cleaned_data['isbn'],
                    page_count=form.cleaned_data['page_count'],
                    photo=form.cleaned_data['photo']
                )
                book.genres.set(form.cleaned_data['genres'])
                return redirect('elib_index')
            except:
                form.add_error(None, 'Ошибка добавления')
            return render(request, 'elib/add_book.html', context={'form': form, 'title': 'Добавление новой книги'})

class BookDetail(DetailView):
    model = Books
    template_name = 'elib/book.html'
    slug_url_kwarg = 'book_slug'
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['book']
        return context

class AddBook(FormView):
    form_class = AddBookForm
    template_name = 'elib/add_book.html'
    success_url = reverse_lazy('elib_index')
    extra_context = {
        'title': 'Добавление книги'
    }
    def form_valid(self, form):
        book = Books.objects.create(
            title=form.cleaned_data['title'],
            author=form.cleaned_data['author'],
            publication_year=form.cleaned_data['publication_year'],
            short_description=form.cleaned_data['short_description'],
            isbn=form.cleaned_data['isbn'],
            page_count=form.cleaned_data['page_count'],
            photo=form.cleaned_data['photo']
        )
        book.genres.set(form.cleaned_data['genres'])
        return super().form_valid(form)