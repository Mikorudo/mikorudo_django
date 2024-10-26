from django.db import models
from django.urls import reverse

class Books(models.Model):
    class Genre(models.TextChoices):
        FICTION = 'fiction', 'Художественная литература'
        MYSTERY = 'mystery', 'Детектив'
        FANTASY = 'fantasy', 'Фэнтези'
        SCIENCE_FICTION = 'science_fiction', 'Научная фантастика'
        BIOGRAPHY = 'biography', 'Биография'
        HISTORY = 'history', 'История'
        ROMANCE = 'romance', 'Роман'
        THRILLER = 'thriller', 'Триллер'
        SELF_HELP = 'self_help', 'Саморазвитие'
        POETRY = 'poetry', 'Поэзия'
        HORROR = 'horror', 'Ужасы'
        ADVENTURE = 'adventure', 'Приключения'
        SCIENCE = 'science', 'Наука'
        ART = 'art', 'Искусство'

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    short_description = models.TextField(blank=True)
    isbn = models.CharField(max_length=17, blank=True)
    page_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True)
    genre = models.CharField(
        max_length=63,
        choices=Genre.choices,
        default=Genre.FICTION,
    )

    objects = models.Manager()

    class Meta:
        ordering = ['title']
        unique_together = ('title', 'author')

    indexes = [
        models.Index(fields=['title']),
    ]

    def get_absolute_url(self):
        return reverse('book_detail_by_slug', kwargs={'book_slug':
                                           self.slug})

    def __str__(self):
        return self.title