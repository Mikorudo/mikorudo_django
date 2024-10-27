from django.utils import timezone

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(date__lt=timezone.now().date())

class UpcomingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(date__gte=timezone.now().date())

class Activities(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, verbose_name='Категория')
    duration = models.DurationField(verbose_name='Длительность')
    contact = models.EmailField(verbose_name='Контакт')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name='Просмотрело')

    objects = models.Manager()
    archived = ArchivedManager()
    upcoming = UpcomingManager()

    class Meta:
        ordering = ['-date', 'time']
        verbose_name = 'Мероприятия'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activity_by_slug', kwargs={'activity_slug':
                                           self.slug})
    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.title))

        unique_slug = slug
        counter = 1
        while Activities.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

class Categories(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категории мероприятий'
        verbose_name_plural = 'Категории мероприятий'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.title))

        self.slug = slug
        super().save(*args, **kwargs)