from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Books(models.Model):
    title = models.CharField(max_length=255,verbose_name='Заголовок')
    author = models.CharField(max_length=255, verbose_name='Автор')
    publication_year = models.PositiveIntegerField(verbose_name='Год публикации')
    short_description = models.TextField(blank=True, verbose_name='Краткое описание')
    isbn = models.OneToOneField('ISBN', on_delete=models.SET_NULL, null=True, blank=True, related_name='book', verbose_name='ISBN')
    page_count = models.IntegerField(verbose_name='Количество страниц')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания страницы')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления страницы')
    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True)
    genres = models.ManyToManyField('Genres', blank=True, related_name='genres', verbose_name='Жанры')

    objects = models.Manager()

    class Meta:
        ordering = ['title']
        unique_together = ('title', 'author')
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'

    indexes = [
        models.Index(fields=['title']),
    ]

    def get_absolute_url(self):
        return reverse('book_detail_by_slug', kwargs={'book_slug':
                                           self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(f"{self.title} {self.author}"))

        unique_slug = slug
        counter = 1
        while Books.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

class Genres(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Жанры книг'
        verbose_name_plural = 'Жанры книг'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.name))

        self.slug = slug
        super().save(*args, **kwargs)


class ISBN(models.Model):
    isbn_number = models.CharField(max_length=13, unique=True, verbose_name='Номер ISBN')

    objects = models.Manager()

    class Meta:
        verbose_name = 'ISBN'
        verbose_name_plural = 'ISBN'

    def formatted_isbn(self):
        if len(self.isbn_number) == 13:
            return f"{self.isbn_number[:3]}-{self.isbn_number[3:4]}-{self.isbn_number[4:9]}-{self.isbn_number[9:12]}-{self.isbn_number[12]}"
        elif len(self.isbn_number) == 10:
            return f"{self.isbn_number[0]}-{self.isbn_number[1:5]}-{self.isbn_number[5:9]}-{self.isbn_number[9]}"
        else:
            return self.isbn_number

    def __str__(self):
        return self.formatted_isbn()

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.__str__()))

        self.slug = slug
        super().save(*args, **kwargs)