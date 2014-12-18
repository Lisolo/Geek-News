from datetime import datetime

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Geek_News.settings')

import django
django.setup()

from share.models import Tag, Book, News
from django.contrib.auth.models import User

user = User.objects.get(username='solo')

def populate():
    python_tag = add_tag('Python')

    add_news(tag=python_tag, user=user,
        title='Understanding decorators',
        url='http://agiliq.com/blog/2012/11/understanding-decorators-2/')

    add_news(tag=python_tag, user=user,
        title='Hopeful Ramble: Web Scraping with Scrapy',
        url='http://hopefulramble.blogspot.ca/2014/08/web-scraping-with-scrapy-first-steps_30.html')

    add_news(tag=python_tag, user=user,
        title='Reducers explained (through Python)',
        url='http://adambard.com/blog/Reducers-explained-through-Python/')

    django_tag = add_tag('Django')

    add_news(tag=django_tag, user=user,
        title='Core Concepts of Django ModelForms',
        url='http://pydanny.com/core-concepts-django-modelforms.html')

    add_news(tag=django_tag, user=user,
        title='Getting Started with Django Rest Framework and AngularJS',
        url='http://blog.kevinastone.com/getting-started-with-django-rest-framework-and-angularjs.html')

    add_news(tag=django_tag, user=user,
        title='An Architecture for Django Templates',
        url='https://oncampus.oberlin.edu/webteam/2012/09/architecture-django-templates')    
    
    add_book(tag=python_tag,
        name='Wikibooks Non-Programmers Tutorial for Python',
        url='http://en.wikibooks.org/wiki/Non-Programmer%27s_Tutorial_for_Python_2.6')

    add_book(tag=python_tag,
        name='Data Structures and Algorithms in Python',
        url='http://www.brpreiss.com/books/opus7/html/book.html',
        author='Bruno R. Preiss')

    add_book(tag=python_tag,
        name='Dive into Python 3',
        url='http://www.diveinto.org/python3')

    add_book(tag=python_tag,
        name='Natural Language Processing with Python',
        url='http://www.nltk.org/book',
        author='Steven Bird, Ewan Klein, and Edward Loper')
    
    add_book(tag=python_tag,
        name='Snake Wrangling For Kids',
        url='http://www.briggs.net.nz/snake-wrangling-for-kids.html',
        author='Allen Downey')

    # Print out what we have added to the user.
    for tag in Tag.objects.all():
        for n in News.objects.filter(tag=tag):
            print('- {0} - {1}'.format(str(tag), str(n)))

        for b in Book.objects.filter(tag=tag):
            print('- {0} - {1}'.format(str(tag), str(b)))

    

def add_tag(name):
    tag = Tag.objects.get_or_create(name=name)[0]
    return tag

def add_news(tag, user, title, url):
    news = News.objects.get_or_create(tag=tag, author=user, title=title, url=url)[0]
    return news

def add_book(tag, name, url, author=''):
    book = Book.objects.get_or_create(tag=tag, name=name, url=url, author=author)

# Start execution here!
if __name__ == '__main__':
    print("Starting Geek News population script...")
    populate()
