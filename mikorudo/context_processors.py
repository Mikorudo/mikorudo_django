from elib.menu import get_elib_menu
from activities.menu import get_activities_menu

def menu_items(request):
    base_menu = [
        {'title':"Главная страница", 'url_name':"index", 'priority':-1},
        {'title':"Обратная связь", 'url_name':"feedback", 'priority':8},
        {'title':"О сайте", 'url_name':"about", 'priority':9},
    ]

    full_menu = base_menu + get_elib_menu() + get_activities_menu()
    full_menu = sorted(full_menu, key=lambda item: item.get('priority', 0))

    return {
        'menu': full_menu
    }