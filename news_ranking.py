import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Startup_News.settings')

import django
django.setup()

from share.models import News

def rank():
	news_list = News.objects.all()
	for news in news_list:
		try:
		    rank = (news.likes - news.dislikes) / news.views
		    news.rank = rank
		except:
			news.rank = 0.00
		news.save()
		print('- {} - {}'.format(str(news), str(news.rank)))

if __name__ == '__main__':
	rank()