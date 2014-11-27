from datetime import datetime

from .models import Category, LikeCategory, News, LikeNews, DislikeNews, Comments, UserProfile, Book
from .bing_search import run_query
from .forms import CategoryForm, NewsForm, CommentsForm, UserForm, UserProfileForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_news_list(max_results=0, starts_with=''):
    news_list = []
    if starts_with:
        news_list = News.objects.filter(title__startswith=starts_with)
    else:
        news_list = News.objects.all()

    if max_results > 0:
        if (len(news_list) > max_results):
            news_list = news_list[:max_results]

    for news in news_list:
        news.url = encode_url(news.title)
    
    return news_list

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    top_category_list = Category.objects.order_by('-likes')[:5]

    for category in top_category_list:
        category.url = encode_url(category.name)

    context_dict = {'categories': top_category_list}

    sugg_list = get_news_list(max_results=5)
    context_dict['news_list'] = sugg_list

    news_list = News.objects.order_by('-views')[:15]
    context_dict['news'] = news_list
    """
    if request.session.get('last_visit'):
    # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    """
    if request.session.get('visits'):
        visits = request.session.get('visits', 0)
        request.session['visits'] = visits + 1
    else:
        request.session['visits'] = 1

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    return render(request, 'index.html', context_dict)

def category(request, category_name_url):
    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = decode_url(category_name_url)

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
    sugg_list = get_news_list(max_results=5)
    context_dict['news_list'] = sugg_list

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        # Retrieve all of the associated News.
        # Note that filter returns >= 1 model instance.
        news_list = News.objects.filter(category=category).order_by('-views')
        
        u = User.objects.get(username=request.user)
        like_list = LikeNews.objects.filter(user=u)
        dislike_list = DislikeNews.objects.filter(user=u)

        for news in news_list:
            news.url = encode_url(news.title)
            try:
                news.comments = Comments.objects.filter(news=news).count()
            except:
                news.comments = None
            
            #determine whether user click the like button
            for x in like_list:
                if news.title == x.news:
                    news.like = True
                    break
                else:
                    news.like = False
            #determine whether user click the dislike button
            for x in dislike_list:
                if news.title == x.news:
                    news.dislike = True
                    break
                else:
                    news.dislike = False

        # Adds our results list to the template context under name News.
        context_dict['news'] = news_list



        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    like_category = LikeCategory.objects.filter(user=u)
    for x in like_category:
        if x.category == category.name: 
            context_dict['like'] = True
            break
        else:
            context_dict['like'] = False
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list

    # Go render the response and return it to the client.
    return render(request, 'category.html', context_dict)

def get_books(request):
    context_dict = {}
    news_list = get_news_list(max_results=5)
    context_dict['news_list'] = news_list

    # Get the books belong to Python.
    try:
        category = Category.objects.get(name='Python')
        python_books = Book.objects.filter(category=category)
        context_dict['python_books'] = python_books
    except:
        context_dict['python_books'] = None

    # Get the books belong to Java.
    try:
        category = Category.objects.get(name='Java')
        java_books = Book.objects.filter(category=category)
        context_dict['java_books'] = java_books
    except:
        context_dict['java_books'] = None

    return render(request, 'books.html', context_dict)

def about(request):
    context_dict = {}
    news_list = get_news_list(max_results=5)
    context_dict['news_list'] = news_list
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.

    count = request.session.get('visits', 0)

    context_dict['visit_count'] = count

    # Return and render the response, ensuring the count is passed to the template engine.
    return render(request, 'about.html', context_dict)

def user_profile(request, author):
    context_dict = {}
    u = User.objects.get(username=author)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    try:
        news_list = News.objects.filter(author=u)
    except:
        news_list = None

    try:
        comments = Comments.objects.filter(user=u)
    except:
        comments = None

    context_dict['another_user'] = u
    context_dict['user_profile'] = up
    context_dict['news'] = news_list
    context_dict['comments'] = comments

    return render(request, 'profile.html', context_dict)

"""
@login_required
def add_category(request):
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list

    # A HTTP POST?
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)

        # Have we been provided with a valid form?
        if category_form.is_valid():
            # Save the new category to the database.
            category_form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homeNew.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()
    
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    context_dict['form'] = form
    return render(request, 'add_category.html', context_dict)
"""

@login_required
def add_news(request, category_name_url):
    sugg_list = get_news_list()
    context_dict = {}
    context_dict['news_list'] = sugg_list

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        news_form = NewsForm(data=request.POST)

        if news_form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            news = news_form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            try:
                cat = Category.objects.get(name=category_name)
                news.category = cat
            except Category.DoesNotExist:
                return render(request, 'add_new.html', context_dict)

            # Also, create a default value for the number of views.
            news.views = 0
            author = User.objects.get(username=request.user)
            # Save the author of news.
            news.author = author
            # Get the current time and save it to news.time.
            news.time = datetime.now().strftime('%Y-%m-%d')
            # With this, we can then save our new model instance.
            news.save()

            # Now that the New is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print(news_form.errors)
    else:
        news_form = NewsForm()

    context_dict['category_name_url'] = category_name_url
    context_dict['category_name'] = category_name
    context_dict['form'] = news_form

    return render(request, 'add_news.html', context_dict)

def add_comments(request, news_title_url):
    context_dict = {}
    news_title = decode_url(news_title_url)
    news = News.objects.get(title=news_title)
    comments = Comments.objects.filter(news=news).order_by('-points')

    context_dict['comments'] = comments

    if request.method == 'POST':
        comments_form = CommentsForm(data=request.POST)
        if comments_form.is_valid():
            new_comments = comments_form.save(commit=False)
            
            user = User.objects.get(username=request.user)
            new_comments.user = user
            new_comments.news = news
            # Get the current time and save it to news.time.
            new_comments.time = datetime.now().strftime('%Y-%m-%d')
            new_comments.points = 0
            # Save the new model instance.
            new_comments.save()

    else:
        comments_form = CommentsForm()

    context_dict['form'] = comments_form
    context_dict['news_title_url'] = news_title_url
    
    return render(request, 'comments.html', context_dict)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Use the login_required() decorator to ensure only those logged in can access the view.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/share/')

@login_required
def profile(request):
    context_dict = {}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
        up.gender = up.get_gender_display()
    except :
        up = None

    try:
        news_list = News.objects.filter(author=u)
    except:
        news_list = None

    try:
        comments = Comments.objects.filter(user=u)
    except:
        comments = None

    context_dict['another_user'] = u
    context_dict['user_profile'] = up
    context_dict['news'] = news_list
    context_dict['comments'] = comments
    return render(request, 'profile.html', context_dict)

@login_required
def like_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()
        u = User.objects.get(username=request.user)
        try:
            like_category = LikeCategory(user=u, category=category.name)
            like_category.save()
        except:
            pass
            
    return HttpResponse(likes)

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.join = datetime.now().strftime('%Y-%m-%d')
            
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(
        request, 
        'register.html', 
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/share/')
            else:
                return HttpResponse("Your Startup News account is disabled.")
        else:
            try:
                user = User.objects.get(username=username)
            except:
                user = None
            if not user:
                user_error = 'User {} does not exit!'.format(username)
                return render(request, 'login.html', {'user_error': user_error})
            else:
                password_error = 'Incorrect password.'
                return render(request, 'login.html', {'password_error': password_error})
            print("Invalid login details: {0}, {1}".format(username, password))
            
    else:
        return render(request, 'login.html', {})

def password_reset(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'password_reset.html', {})

def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'search.html', {'result_list': result_list})

@login_required
def likes_news(request):
    if request.method == 'GET':
        cat_id = request.GET['new_id']

    likes = 0
    if cat_id:
        news = News.objects.get(id=int(cat_id))
        # Get the current user
        u = User.objects.get(username=request.user)
        # Save liked news to the database.
        like_news = LikeNews(user=u, news=news.title)
        like_news.save()
        if news:
            likes = news.likes + 1
            news.likes = likes
            news.save()
            
    return HttpResponse(likes)

@login_required
def dislikes_news(request):
    if request.method == 'GET':
        cat_id = request.GET['new_id']

    dislikes = 0
    if cat_id:
        news = News.objects.get(id=int(cat_id))
        # Get the current user
        u = User.objects.get(username=request.user)
        # Save disliked news to the database.
        dislike_news = DislikeNews(user=u, news=news.title)
        dislike_news.save()
        if news:
            dislikes = news.dislikes + 1
            news.dislikes = dislikes
            news.save()
            
    return HttpResponse(dislikes)

def track_url(request):
    new_id = None
    url = '/share/'
    if request.method == 'GET':
        if 'new_id' in request.GET:
            new_id = request.GET['new_id']
            try:
                news = News.objects.get(id=new_id)
                news.views = news.views + 1
                news.save()
                url = news.url
            except :
                pass

    return redirect(url)

def suggest_news(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    else:
        starts_with = request.POST['suggestion']

    news_list = get_news_list(8, starts_with)

    return render(request, 'news_list.html', {'news_list': news_list})

@login_required
def auto_add_new(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = New.objects.get_or_create(category=category, title=title, url=url)

            News = New.objects.filter(category=category).order_by('-views')
            
            # Adds our results list to the template context under name News.
            context_dict['News'] = News

    return render(request, 'New_list.html', context_dict)