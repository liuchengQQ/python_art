from django.shortcuts import render,get_object_or_404
from .models import BlogArticles

def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request,"blog/titles.html",{"blogs":blogs})

def blog_article(request,id):
    # artic = BlogArticles.objects.get(id=id)
    artic = get_object_or_404(BlogArticles,id=id)
    pub = artic.publish
    return render(request,"blog/content.html",{"article":artic,"publish":pub})
