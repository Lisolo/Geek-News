from datetime import datetime

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Startup_News.settings')

import django
django.setup()

from share.models import Category, News
from django.contrib.auth.models import User

user = User.objects.get(username='solo')
time = datetime.now().strftime('%Y-%m-%d')

def populate():
    python_cat = add_cat('Python')

    add_news(cat=python_cat, user=user,
        title='Understanding decorators',
        url='http://agiliq.com/blog/2012/11/understanding-decorators-2/',
        time=time)

    add_news(cat=python_cat, user=user,
        title='Hopeful Ramble: Web Scraping with Scrapy',
        url='http://hopefulramble.blogspot.ca/2014/08/web-scraping-with-scrapy-first-steps_30.html',
        time=time,)

    add_news(cat=python_cat, user=user,
        title='Reducers explained (through Python)',
        url='http://adambard.com/blog/Reducers-explained-through-Python/',
        time=time)

    django_cat = add_cat('Django')

    add_news(cat=django_cat, user=user,
        title='Core Concepts of Django ModelForms',
        url='http://pydanny.com/core-concepts-django-modelforms.html',
        time=time)

    add_news(cat=django_cat, user=user,
        title='Getting Started with Django Rest Framework and AngularJS',
        url='http://blog.kevinastone.com/getting-started-with-django-rest-framework-and-angularjs.html',
        time=time)

    add_news(cat=django_cat, user=user,
        title='An Architecture for Django Templates',
        url='https://oncampus.oberlin.edu/webteam/2012/09/architecture-django-templates',
        time=time)    

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for n in News.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(n)))

def add_news(cat, user, title, url, time):
    p = News.objects.get_or_create(category=cat, author=user, title=title, url=url, time=time)[0]
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
