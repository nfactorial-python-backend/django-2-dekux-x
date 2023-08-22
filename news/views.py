from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group


from .models import News, Comment
from .forms import AddPostNews, AddPostComment, SignUpForm


# Create your views here.
def index(request):
    newss = News.objects.order_by("-created_at").all()
    context = {
        "newss": newss
    }
    return render(request,"news/index.html",context)

def detail(request,news_id: int):
    if request.method == "POST":
        form = AddPostComment(request.POST)
        if form.is_valid():
            try:
                news = News.objects.get(pk=news_id)
            except News.DoesNotExist:
                raise Http404("Not found") 
            news.comment_set.create(content = form.cleaned_data["content"], author = request.user)
            return redirect(f'/news/{news_id}/')
        
    else:
        form = AddPostComment
    try:
        news = News.objects.get(pk=news_id)
        comments = Comment.objects.filter(news_id=news_id).order_by("-created_at").all()
    except News.DoesNotExist:
        raise Http404("Not found")  
    context = {"news": news, "comments": comments, "form": form, "auth": request.user.is_authenticated}
    return render(request, "news/detail.html", context)

@login_required(login_url="/login/")
@permission_required("news.add_news", login_url="/login/")
def create(request):
    if request.method == "POST":
        form = AddPostNews(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return HttpResponseRedirect(reverse("news:index"))
    form = AddPostNews
    return render(request, "news/create.html", {"form": form})

class NewsEdit(View):
    @method_decorator(permission_required("news.change_news", login_url="/login/"))
    def get(self, request, news_id: int):
        form = AddPostNews
        news = get_object_or_404(News, pk=news_id)
        return render(request, "news/edit.html", {"form": form, "news": news})
        
    @method_decorator(permission_required("news.change_news", login_url="/login/"))
    def post(self,request, news_id: int):
        form = AddPostNews(request.POST)
        if form.is_valid():
            news = get_object_or_404(News, pk=news_id)
            news.title = form.cleaned_data["title"]
            news.content = form.cleaned_data["content"]
            news.save()
            return HttpResponseRedirect(reverse("news:index"))
        return render(request, "news/edit.html", {"form": form, "news": news})
    
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(nabe = "default")
            group.user_set.add(user)
            login(request,user)
            return HttpResponseRedirect(reverse("news:index"))
    else:
        form = SignUpForm()
    
    return render(request, "registration/sign_up.html", {"form": form})

@permission_required("news.delete_news", login_url="/login/")
def delete_news(request, news_id: int):
    news = get_object_or_404(News, pk = news_id)
    if request.method == "POST":
        if news.author == request.user or request.user.has_perm("news.delete_news"):
            news.delete()
    return HttpResponseRedirect(reverse("news:index"))

@permission_required("news.delete_comment", login_url="/login/")
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, pk = comment_id)
    news = comment.news_id
    if request.method == "POST":
        if comment.author == request.user or request.user.has_perm("news.delete_comment"):
            comment.delete()
    return HttpResponseRedirect(reverse("news:detail",args=(news.id,)))