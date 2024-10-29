from django.urls import path
from activities import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='activities_index'),
    path('by_id/<int:activity_id>/', views.activity_by_id, name='activity_by_id'),
    path('by_slug/<slug:activity_slug>/', views.activity_by_slug, name='activity_by_slug'),
    path('category/<slug:category_slug>/', views.activities_by_category, name='activities_by_category'),
    path('archive/<int:year>/<int:month>/', views.archive, name='activities_archive'),
    path('add/', views.add_activity, name='add_activity'),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Мероприятия библиотеки"