from django.urls import reverse
from django.db import models

class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    short_description = models.TextField(blank=True)
    isbn = models.OneToOneField('ISBN', on_delete=models.SET_NULL, null=True, blank=True, related_name='book')
    page_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True)
    genres = models.ManyToManyField('Genres', blank=True, related_name='genres')

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

class Genres(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return self.name



class ISBN(models.Model):
    isbn_number = models.CharField(max_length=13, unique=True)

    objects = models.Manager()

    def formatted_isbn(self):
        if len(self.isbn_number) == 13:
            return f"{self.isbn_number[:3]}-{self.isbn_number[3:4]}-{self.isbn_number[4:9]}-{self.isbn_number[9:12]}-{self.isbn_number[12]}"
        elif len(self.isbn_number) == 10:
            return f"{self.isbn_number[0]}-{self.isbn_number[1:5]}-{self.isbn_number[5:9]}-{self.isbn_number[9]}"
        else:
            return self.isbn_number

    def __str__(self):
        return self.formatted_isbn()