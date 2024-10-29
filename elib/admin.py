from django.contrib import admin
from django.utils.safestring import mark_safe

from elib.models import Books, Genres, ISBN

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'page_count', 'book_photo', 'created_at', 'updated_at', 'updated', 'description_length')
    list_display_links = ('id', 'title')
    list_per_page = 5
    ordering = ('updated_at',)
    actions = ['set_default_description']
    search_fields = ('title__startswith', 'author', 'isbn__isbn_number')
    list_filter = ('page_count', 'genres')
    exclude = ['created_at', 'updated_at']
    readonly_fields = ['slug', 'book_photo']

    @admin.display(description='Страница отредактирована')
    def updated(self, book: Books):
        return book.updated_at != book.created_at

    @admin.display(description='Изображение')
    def book_photo(self, book:Books):
        if book.photo:
            return mark_safe(f"<img src='{book.photo.url}' width=50>")
        return "Нет фото"

    @admin.display(description='Размер описания')
    def description_length(self, book:Books):
        return f"Описание книги из ({len(book.short_description)}) символов"

    @admin.action(description="Установить описание по умолчанию")
    def set_default_description(self, request, queryset):
        count = queryset.update(short_description='Описание книги в разработке. Обязательно загляните позже!')
        self.message_user(request, f"Изменено {count} записи(ей).")

@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ('name',)

@admin.register(ISBN)
class ISBNAdmin(admin.ModelAdmin):
    list_display = ('id', 'isbn_number')
    list_display_links = ('id', 'isbn_number')
    ordering = ('isbn_number',)
