from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'share.views.index', name='index'),
    url(r'^books/$', 'share.views.get_books', name='book'),
    url(r'^about/$', 'share.views.about', name='about'),
    url(r'^search/$', 'share.views.search', name='search'),
    url(r'^login/$', 'share.views.user_login', name='login'),
    url(r'^profile/$', 'share.views.profile', name='profile'),
    url(r'^goto/$', 'share.views.track_url', name='track_url'),
    url(r'^logout/$', 'share.views.user_logout', name='logout'),
    url(r'^register/$', 'share.views.register', name='register'),
    url(r'^restricted/$', 'share.views.restricted', name='restricted'),
    # url(r'^add_category/$', 'share.views.add_category', name='add_category'),
    url(r'^like_new/$', 'share.views.like_new', name='like_new'),
    url(r'^dislike_new/$', 'share.views.dislike_new', name='dislike_new'),
    url(r'^like_category/$', 'share.views.like_category', name='like_category'),
    url(r'^auto_add_page/$', 'share.views.auto_add_new', name='auto_add_new'),
    url(r'^password_reset/$', 'share.views.password_reset', name='password_reset'),
    url(r'^suggest_news/$', 'share.views.suggest_news', name='suggest_category'),
    url(r'^category/(?P<category_name_url>\w+)/$', 'share.views.category', name='category'),
    url(r'^user/(?P<author>\w+)/$', 'share.views.user_profile', name='user_profile'),
    url(r'^add_comments/(?P<news_title_url>\w+)/$', 'share.views.add_comments', name='add_comments'),
    url(r'^category/(?P<category_name_url>\w+)/add_news/$', 'share.views.add_news', name='add_new'),
)