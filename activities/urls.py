from django.urls import path
from activities import views
from django.contrib import admin

urlpatterns = [
    path('', views.HomeActivityView.as_view(), name='activities_index'),
    path('by_id/<int:activity_id>/', views.ActivityDetail.as_view(), name='activity_by_id'),
    path('by_slug/<slug:activity_slug>/', views.ActivityDetail.as_view(), name='activity_by_slug'),
    path('category/<slug:category_slug>/', views.ActivityCategory.as_view(), name='activities_by_category'),
    path('archive/<int:year>/<int:month>/', views.ActivityArchive.as_view(), name='activities_archive'),
    path('add/', views.AddActivity.as_view(), name='add_activity'),
    path('edit/<int:pk>/', views.UpdateActivity.as_view(), name='edit_activity_by_id'),
    path('edit/<slug:slug>/', views.UpdateActivity.as_view(), name='edit_activity_by_slug'),
    path('delete/<int:pk>/', views.DeleteActivity.as_view(), name='delete_activity_by_slug'),
    path('delete/<slug:slug>/', views.DeleteActivity.as_view(), name='delete_activity_by_slug'),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Мероприятия библиотеки"