def get_activities_menu(request):
    arr =  [
        {'title': "Мероприятия", 'url_name': "activities_index"}
    ]
    if request.user.has_perm('activities.add_books'):
        arr.append(
            {'title': "Создать мероприятие", 'url_name': "add_activity"}
        )
    return arr