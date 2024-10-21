from django.shortcuts import render, get_object_or_404
from datetime import datetime

# Заглушка для мероприятий
activities = [
    {
        'id': 0,
        'title': 'Python Workshop',
        'description': 'A workshop on Python programming basics.',
        'date': '2024-11-01',
        'time': '10:00',
        'location': 'Tech Hub, Room 101',
        'categories': ['Programming', 'Workshops'],
        'duration': '2 hours',
        'contact': 'python@techhub.com',
    },
    {
        'id': 1,
        'title': 'Data Science Meetup',
        'description': 'Discussion about trends in Data Science.',
        'date': '2024-11-05',
        'time': '15:00',
        'location': 'Main Hall, Tech Center',
        'categories': ['Data Science', 'Meetups'],
        'duration': '3 hours',
        'contact': 'datascience@techcenter.com',
    },
    {
        'id': 2,
        'title': 'AI in Healthcare',
        'description': 'Exploring the use of AI in the medical field.',
        'date': '2024-11-10',
        'time': '13:00',
        'location': 'Health Center, Room 202',
        'categories': ['AI', 'Healthcare'],
        'duration': '4 hours',
        'contact': 'aihealth@healthcenter.com',
    },
]

def index(request):
    return render(request, 'activities/activities_list.html', {'activities': activities[:20]})

def activity_by_id(request, id):
    activity = next((act for act in activities if act['id'] == id), None)
    if activity is None:
        return render(request, '404.html', status=404)
    return render(request, 'activities/activity.html', {'activity': activity})

def archive(request, year, month):
    filtered_activities = [
        act for act in activities
        if datetime.strptime(act['date'], '%Y-%m-%d').year == year and
           datetime.strptime(act['date'], '%Y-%m-%d').month == month
    ]
    return render(request, 'activities/archive.html', {'activities': filtered_activities, 'year': year, 'month': month})
