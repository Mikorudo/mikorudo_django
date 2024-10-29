from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render

from elib.models import UploadFiles
from .forms import UploadFileForm


def index(request):
    data = {
        'title': 'Главная страница'
    }
    return render(request, 'index.html', data)

def feedback(request):
    data = {
        'title': 'Обратная связь'
    }
    return render(request, 'feedback.html', data)

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'about.html', context = {'title': 'О сайте', 'form': form})

#Обработчики исключений
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Запрашиваемая странице не найдена</h1>')

def forbidden(request, exception):
    return HttpResponseForbidden('<h1>Доступ запрещён</h1>')

def bad_request(request, exception):
    return HttpResponseBadRequest('<h1>Некорректный запрос</h1>')

def internal_server_error(request):
    return HttpResponseServerError('<h1>Ошибка сервера. Обратитесь к администратору</h1>')
