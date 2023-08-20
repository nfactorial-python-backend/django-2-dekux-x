from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def has_comments(self):
        comment = Comment.objects.filter(news_id = self.id).first()
        if comment:
            return True
        return False
    
class Comment(models.Model):
    news_id = models.ForeignKey(News,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)