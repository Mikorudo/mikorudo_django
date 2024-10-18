from django.urls import path, register_converter
from activities import views
from activities import converters

register_converter(converters.DateConverter, 'dateC')

urlpatterns = [
    path('', views.index, name='activities_index'),
    path('by_date/<dateC:date>/', views.activities_of_date, name='activities_by_date'),
    path('by_id/<int:id>/', views.activity_by_id, name='activity_by_id'),
    path('archive/<int:year>/<int:month>/', views.archive, name='activities_archive')
]