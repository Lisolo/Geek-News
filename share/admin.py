from django.contrib import admin

from .models import Category, LikeCategory, News, LikeNews, DislikeNews, Comments, VoteComments, Book, UserProfile


admin.site.register(Category)
admin.site.register(LikeCategory)
admin.site.register(News)
admin.site.register(LikeNews)
admin.site.register(DislikeNews)
admin.site.register(Comments)
admin.site.register(VoteComments)
admin.site.register(UserProfile)
admin.site.register(Book)