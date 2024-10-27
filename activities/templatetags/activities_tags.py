from django import template
from django.db.models import Count

from activities.models import Activities, Categories

register = template.Library()

@register.inclusion_tag('activities/upcoming_activities.html')
def get_upcoming_activities(count=5):
    upcoming_activities = Activities.upcoming.all().order_by('date')[:count]
    return {'activities': upcoming_activities}

@register.inclusion_tag('activities/activity_categories.html')
def get_activity_categories():
    activity_categories = Categories.objects.annotate(activity_count=Count('activities')).filter(activity_count__gt=0)
    return {'activity_categories': activity_categories}