from django.contrib import admin

from .models import Category, LikeCategory, News, Comments, Book, UserProfile


admin.site.register(Category)
admin.site.register(LikeCategory)
admin.site.register(News)
admin.site.register(Comments)
admin.site.register(UserProfile)
admin.site.register(Book)