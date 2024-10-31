"""
URL configuration for mikorudo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mikorudo import views, settings

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin/', admin.site.urls, name = 'admin'),
    path('elib/', include('elib.urls')),
    path('activities/', include('activities.urls')),
    path('users/', include('users.urls', namespace='users'), )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = views.bad_request
handler403 = views.forbidden
handler404 = views.page_not_found
handler500 = views.internal_server_error