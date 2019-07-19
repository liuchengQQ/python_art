from django.conf.urls import url
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    url(r"^login/$",views.user_login,name="user_login"),
    url(r"^register/$",views.register,name="register"),
    url(r"^myself/$",views.myself,name="myself"),
    url(r"^myself_Edit/$", views.myself_edit, name="myself_Edit"),
    url(r"^my_images/$", views.my_images, name="my_images"),
    url(r"^logout/$",LogoutView.as_view(template_name='account/logout.html'),name="user_logout"),
]

