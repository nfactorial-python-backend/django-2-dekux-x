from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.index, name='index'),
    path("<int:news_id>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path("<int:news_id>/edit/", views.NewsEdit.as_view(), name="edit"),
]