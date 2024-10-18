from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from django.urls import reverse


# Create your views here.
def activities_of_date(request, date):
    current_date = datetime.now().date()
    if date < current_date:
        url_redirect = reverse('activities_archive', args=(date.year, date.month))
        return HttpResponseRedirect(url_redirect)
    return HttpResponse(f"<h1>Мероприятия: </h1><p>На дату:{date}</p>")


def activity_by_id(request, id):
    return HttpResponse(f"<h1>Мероприятия: </h1><p>Идентификатор:{id}</p>")


def index(request):
    return HttpResponse(f"<h1>Главная страница мероприятий</h1>")


def archive(request, year, month):
    return HttpResponse(f"<h1>Архив мероприятий за {month}/{year}</h1>")