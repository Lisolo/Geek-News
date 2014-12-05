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
    views = models.IntegerField(default=0)

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
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.user.username + '-' + self.category.name

class Book(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    author = models.CharField(max_length=128, blank=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class LikeBook(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.user.username + '-' + self.book.name

class News(models.Model):
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    time = models.DateField()
    rank = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    def __str__(self):
        return self.title

class LikeNews(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)

    def __str__(self):
        return self.user.username + '-' + self.news.title

class DislikeNews(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)

    def __str__(self):
        return self.user.username + '-' + self.news.title  

class Comments(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)
    content = models.TextField()
    time = models.DateTimeField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class VoteComments(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comments)

    def __str__(self):
        return self.user.username + '-' + self.comment.content
