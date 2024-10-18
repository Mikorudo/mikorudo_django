from django.http import HttpResponse, Http404
from datetime import datetime

def index(request):
    return HttpResponse("Страница приложения elib")

def book_by_id(request, id):
    return HttpResponse(f"<h1>Электронная книга: </h1><p>Идентификатор:{id}</p>")

def book_by_title(request, title):
    if request.method == "GET":
        print(request.GET)
    return HttpResponse(f"<h1>Электронная книга: </h1><p>Название:{title}</p>")

def books_by_year(request, year):
    current_year = datetime.now().year
    if year > current_year:
        raise Http404()
    return HttpResponse(f"<h1>Электронные книги: </h1><p>Год:{year}</p>")