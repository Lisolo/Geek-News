from django.contrib import admin

from .models import *


admin.site.register(Tag)
admin.site.register(KeyWord)
admin.site.register(LikeTag)
admin.site.register(News)
admin.site.register(LikeNews)
admin.site.register(DislikeNews)
admin.site.register(Comments)
admin.site.register(VoteComments)
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(LikeBook)