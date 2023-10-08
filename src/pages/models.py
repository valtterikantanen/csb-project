from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    book_title = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    rating = models.IntegerField()
    review_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_text
