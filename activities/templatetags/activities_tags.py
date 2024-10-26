from django import template
from activities.models import Activities

register = template.Library()

@register.inclusion_tag('activities/upcoming_activities.html')
def get_upcoming_activities(count=5):
    upcoming_activities = Activities.upcoming.all().order_by('date')[:count]
    return {'activities': upcoming_activities}