from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from .models import News, Comment
from .forms import AddPostNews, AddPostComment


# Create your views here.
def index(request):
    newss = News.objects.order_by("-created_at").all()
    context = {
        "newss": newss
    }
    return render(request,"news/index.html",context)

def detail(request,news_id: int):
    if request.method == "POST":
        inform = dict(request.POST)
        try:
            news = News.objects.get(pk=news_id)
        except News.DoesNotExist:
            raise Http404("Not found") 
        news.comment_set.create(content = inform["content"][0])
        return redirect(f'/news/{news_id}/')
    form = AddPostComment
    try:
        news = News.objects.get(pk=news_id)
        comments = Comment.objects.filter(news_id=news_id).order_by("-created_at").all()
    except News.DoesNotExist:
        raise Http404("Not found")  
    context = {"news": news, "comments": comments, "form": form}
    return render(request, "news/detail.html", context)

def create(request):
    if request.method == "POST":
        form = AddPostNews(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("news:index"))
    form = AddPostNews
    return render(request, "news/create.html", {"form": form})

class NewsEdit(View):
    def get(self, request, news_id: int):
        form = AddPostNews
        news = get_object_or_404(News, pk=news_id)
        return render(request, "news/edit.html", {"form": form, "news": news})
    def post(self,request, news_id: int):
        form = AddPostNews(request.POST)
        if form.is_valid():
            news = get_object_or_404(News, pk=news_id)
            news.title = form.cleaned_data["title"]
            news.content = form.cleaned_data["content"]
            news.save()
            return HttpResponseRedirect(reverse("news:index"))
        return render(request, "news/edit.html", {"form": form, "news": news})