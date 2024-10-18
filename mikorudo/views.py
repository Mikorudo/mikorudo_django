from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Запрашиваемая странице не найдена</h1>')

def forbidden(request, exception):
    return HttpResponseForbidden('<h1>Доступ запрещён</h1>')

def bad_request(request, exception):
    return HttpResponseBadRequest('<h1>Некорректный запрос</h1>')

def internal_server_error(request):
    return HttpResponseServerError('<h1>Ошибка сервера. Обратитесь к администратору</h1>')