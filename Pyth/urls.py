"""Pyth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
# from blog import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',views.index),
    # path('/<name>',views.index),
    url(r'^admin/',admin.site.urls),
    url(r'^blog/',include(('blog.urls','blog'),namespace='blog')),
    url(r'^account/',include(('account.urls','account'),namespace='account')),
    url(r'^article/',include(('article.urls','article'),namespace='article')),
    url(r'^home/',TemplateView.as_view(template_name="home.html"),name='home'),
    url(r'^image/',include(('image.urls','image'),namespace='image')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)