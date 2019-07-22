from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^list_images/$',views.list_images,name="list_images"),
    url(r'^upload_images/$',views.upload_image,name="upload_images"),
    url(r'^del_image/$',views.del_image,name="del_image"),
]