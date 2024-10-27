from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from activities.models import Activities
from django.utils.text import slugify
from unidecode import unidecode
from django.db.models import Q, F, Value


def index(request):
    activities = Activities.objects.all()
    return render(request, 'activities/activities_list.html', {'activities': activities})

def activity_by_id(request, activity_id):
    activity = get_object_or_404(Activities, pk=activity_id)
    activity.view_count = F('view_count') + 1
    activity.save()
    return render(request, 'activities/activity.html', {'activity': activity})

def activity_by_slug(request, activity_slug):
    activity = get_object_or_404(Activities, slug=activity_slug)
    activity.view_count = F('view_count') + 1
    activity.save()
    return render(request, 'activities/activity.html', {'activity': activity})

def activities_by_category(request, category_slug):
    activities = Activities.objects.order_by().filter(category__slug=category_slug)
    return render(request, 'activities/activities_list.html', {'activities': activities})

def archive(request, year, month):
    activities = Activities.archived.filter(Q(date__year=year) & Q(date__month=month)).annotate(passed = Value(True))
    return render(request, 'activities/activities_list.html',
                  {'activities': activities, 'year': year, 'month': month})

def create_activity(title, description, date, time, category, duration, contact):
    slug = slugify(unidecode(title))

    unique_slug = slug
    counter = 1
    while Activities.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    activity = Activities.objects.create(
        title=title,
        description=description,
        date=date,
        time=time,
        category=category,
        duration=timedelta(minutes=duration),
        contact=contact,
        slug=unique_slug
    )
    return activity

def update_activity(activity_id, **kwargs):
    activity = get_object_or_404(Activities, pk=activity_id)

    for key, value in kwargs.items():
        if hasattr(activity, key):
            setattr(activity, key, value)

    if 'title' in kwargs:
        slug = slugify(unidecode(kwargs['title']))
        unique_slug = slug
        counter = 1
        while Activities.objects.filter(slug=unique_slug).exclude(id=activity_id).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        activity.slug = unique_slug

    activity.save()
    return activity

def delete_activity(activity_id):
        activity = get_object_or_404(Activities, pk=activity_id)
        activity.delete()