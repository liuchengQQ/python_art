from .models import ArticleColumn,ArticlePost,Comment,ArticleTag
from django import forms

class ArticleColumnForm(forms.ModelForm):

    class Meta:
        model = ArticleColumn
        fields = ("column",)


class ArticlePostForm(forms.ModelForm):

    class Meta:
        model = ArticlePost
        fields = ("title","body")

class CommentForm(forms.Form):

    class Meta:
         model = Comment
         fields = ("commentor","body",)

class ArticleTagForm(forms.Form):

    class Meta:
        model = ArticleTag
        fields = ('tag',)
