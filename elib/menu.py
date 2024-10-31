def get_elib_menu(request):
    arr =  [
        {'title': "Электронная библиотека", 'url_name': "elib_index"}
    ]
    if request.user.has_perm('elib.add_books'):
        arr.append(
            {'title': "Добавить книгу", 'url_name': "add_book"}
        )
    return arr