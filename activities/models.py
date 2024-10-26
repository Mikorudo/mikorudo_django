from django.utils import timezone

from django.db import models
from django.urls import reverse

class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(date__lt=timezone.now().date())

class UpcomingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(date__gte=timezone.now().date())

class Activities(models.Model):
    class Category(models.TextChoices):
        LITERARY_EVENT = 'Literary', 'Литературное мероприятие'
        WORKSHOP = 'Workshop', 'Мастер-класс'
        BOOK_CLUB = 'BookClub', 'Книжный клуб'
        AUTHOR_VISIT = 'AuthorVisit', 'Встреча с автором'
        CHILDREN_EVENT = 'ChildrenEvent', 'Мероприятие для детей'
        LECTURE = 'Lecture', 'Лекция'
        EXHIBITION = 'Exhibition', 'Выставка'
        DISCUSSION = 'Discussion', 'Обсуждение'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    category = models.CharField(
        max_length=63,
        choices=Category.choices,
        default=Category.LITERARY_EVENT,
    )
    duration = models.DurationField()
    contact = models.EmailField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    objects = models.Manager()
    archived = ArchivedManager()
    upcoming = UpcomingManager()

    class Meta:
        ordering = ['-date', 'time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activity_by_slug', kwargs={'activity_slug':
                                           self.slug})