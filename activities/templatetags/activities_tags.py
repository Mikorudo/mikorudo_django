from datetime import datetime

from django import template
from activities.views import activities

register = template.Library()

@register.inclusion_tag('activities/upcoming_activities.html')
def get_upcoming_activities(count=5):
    upcoming_activities = sorted(activities, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    return {'activities': upcoming_activities[:count]}