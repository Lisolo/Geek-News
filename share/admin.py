from django.contrib import admin

from .models import Category, News, Comments, Book, UserProfile


admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comments)
admin.site.register(UserProfile)
admin.site.register(Book)