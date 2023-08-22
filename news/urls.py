from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.index, name='index'),
    path("<int:news_id>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path("<int:news_id>/edit/", views.NewsEdit.as_view(), name="edit"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("<int:news_id>/delete_news/", views.delete_news, name="delete_news"),
    path("<int:comment_id>/delete_comment/", views.delete_comment, name="delete_comment"),


]