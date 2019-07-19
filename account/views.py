from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm
from .forms import ResiterForm
from django.contrib.auth.decorators import login_required
from .models import UserInfo
from django.contrib.auth.models import User
from .forms import UserInfoForm,UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def user_login(request):
     if request.method == "POST":
         login_form = LoginForm(request.POST)
         if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user:
                 login(request,user)
                 return HttpResponse("欢迎来到迪士尼世界")
            else:
                 return HttpResponse("您的用户或密码不正确")
         else:
             return HttpResponse("无效的登陆")
     if request.method == "GET":
        login_form = LoginForm()
        print(login_form)
        return render(request,"account/login.html",{"form":login_form})

def register(request):
    if request.method == "POST":
       user_form = ResiterForm(request.POST)
       if user_form.is_valid():
           new_user = user_form.save(commit=False)
           new_user.set_password(user_form.cleaned_data['password'])
           new_user.save()
           UserInfo.objects.create(user=new_user)
           return HttpResponseRedirect(reverse("account:user_login"))
       else:
           return HttpResponse("对不起，您不能注册")

    else:
        user_form = ResiterForm()
        return render(request,"account/register.html",{"form":user_form})

@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userInfo = UserInfo.objects.get(user=user)
    return render(request,"account/myself.html",{"user":user,"userInfo":userInfo})

@login_required(login_url='/account/login/')
def myself_edit(request):
     user = User.objects.get(username=request.user.username)
     userInfo = UserInfo.objects.get(user=request.user)

     if request.method == "POST":
            user_form = UserForm(request.POST)
            userInfo_form = UserInfoForm(request.POST)
            if user_form.is_valid()*userInfo_form.is_valid():
                user_cd = user_form.cleaned_data
                info_cd = userInfo_form.cleaned_data
                user.email = user_cd['email']
                userInfo.school = info_cd['school']
                userInfo.address = info_cd['address']
                userInfo.aboutme = info_cd['aboutme']
                user.save()
                userInfo.save()
                return HttpResponseRedirect('/account/myself.html')
     else:
         user_form = UserForm(instance=request.user)
         userInfo_form = UserInfoForm(initial={"school": userInfo.school, "address": userInfo.address, "aboutme": userInfo.aboutme})
         return render(request, "account/myself_edit.html", {"user_form": user_form, "userInfo_form": userInfo_form})


@login_required(login_url="/account/login/")
def my_images(request):
    if request.method == "POST":
        img = request.POST['img']
        userInfo = UserInfo.objects.get(user=request.user.id)
        userInfo.photo = img
        userInfo.save()
        return HttpResponse("1")
    else:
        return render(request,"account/imagecrop.html",)



