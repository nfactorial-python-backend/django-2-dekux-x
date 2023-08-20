from django.contrib import admin

# Register your models here.
from .models import News, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5

class AdminNews(admin.ModelAdmin):
    fields = ["title", "content"]
    list_display = ["title", "content", "created_at", "has_comments"]
    inlines = [CommentInline]
    list_filter = ["title"]


admin.site.register(News, AdminNews)