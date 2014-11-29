from django.db import models

from django.contrib.auth.models import User 


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        )
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    join = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class LikeCategory(models.Model):
    user = models.ForeignKey(User)
    category = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.user.username + '-' + self.category

class Book(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    author = models.CharField(max_length=128, blank=True)
    
    def __str__(self):
        return self.name

class News(models.Model):
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    time = models.DateField()

    def __str__(self):
        return self.title

class LikeNews(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)
    content = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username + '-' + self.news.title

class DislikeNews(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)
    content = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username + '-' + self.news.title  

class Comments(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)
    content = models.TextField()
    time = models.DateField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class VoteComments(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comments)
    commentid = models.IntegerField()

    def __str__(self):
        return self.user.username + '-' + self.comment.content
