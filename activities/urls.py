from django.urls import path
from activities import views

urlpatterns = [
    path('', views.index, name='activities_index'),
    path('by_id/<int:id>/', views.activity_by_id, name='activity_by_id'),
    path('archive/<int:year>/<int:month>/', views.archive, name='activities_archive')
]