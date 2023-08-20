from django.test import TestCase
from django.utils import timezone

from .models import News, Comment
import base64

# Create your tests here.
class NewsTests(TestCase):
    def test_has_comments(self):
        news = News(title = "Итоги конкурса грантов стали известны", content =  "Стали известны обладатели грантов 2023 года") 
        news.save()
        news.comment_set.create(content = "Ура я получил грант")    
        self.assertIs(True, news.has_comments())

    def test_has_not_comments(self):
        news = News(title = "Итоги конкурса грантов стали известны", content =  "Стали известны обладатели грантов 2023 года") 
        self.assertIs(False, news.has_comments())
    
    def test_index(self):
        news1 = News(title = "Итоги конкурса грантов стали известны", content =  "Стали известны обладатели грантов 2023 года") 
        news2 = News(title = "DevOps Day в Алматы", content = "Уже в сентябре в Алматы состоится DevOps Day")
        news1.save()
        news2.save()
        response = self.client.get("/news/")
        self.assertQuerysetEqual([news2,news1], response.context["newss"])

    def test_detail(self):
        news1 = News(title = "Итоги конкурса грантов стали известны", content =  "Стали известны обладатели грантов 2023 года")
        news1.save()
        response = self.client.get("/news/1/")
        title = news1.title.encode("utf-8")
        self.assertIn(title,response.content)
        content = news1.content.encode("utf-8")
        self.assertIn(content,response.content)
        
    def test_detail_comments(self):
        news1 = News(title = "Итоги конкурса грантов стали известны", content =  "Стали известны обладатели грантов 2023 года")
        news1.save()
        comment1 = news1.comment_set.create(content = "Ура я получил грант")
        comment2 =  news1.comment_set.create(content = "Я тоже")
        response = self.client.get("/news/1/")
        print(response.content)
        self.assertContains(response, comment1.content.encode())
        self.assertContains(response, comment2.content.encode())
        
