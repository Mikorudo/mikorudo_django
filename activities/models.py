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
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    category = models.ForeignKey('Categories', on_delete=models.PROTECT)
    duration = models.DurationField()
    contact = models.EmailField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

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

class Categories(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
