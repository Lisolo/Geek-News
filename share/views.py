from datetime import datetime
from random import choice

from .models import Category, LikeCategory, News, LikeNews, DislikeNews, Comments, VoteComments, UserProfile, Book, LikeBook
from .bing_search import run_query
from .forms import CategoryForm, NewsForm, CommentsForm, UserForm, UserProfileForm, CaptchaTestForm, reset_form

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from Startup_News.settings import DEFAULT_FROM_EMAIL

from django.views.generic import *
from .forms import PasswordResetRequestForm
from django.contrib import messages

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_news_list(query=''):
    news_list = []
    if query:
        news_list = News.objects.filter(title__icontains=query)[:5]
    else:
        news_list = News.objects.order_by('-views')[:10]
    for news in news_list:
        news.url = encode_url(news.title)
    return news_list

def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'search.html', {'result_list': result_list})

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
    query = ''
    if request.method == 'GET':
        query = request.GET['suggestion']
    else:
        query = request.POST['suggestion']
    news_list = get_news_list(query)
    return render(request, 'news_list.html', {'news_list': news_list})

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    top_category_list = Category.objects.order_by('-likes')[:5]
    for category in top_category_list:
        category.url = encode_url(category.name)
    context_dict = {'categories': top_category_list}
    sugg_list = get_news_list()
    context_dict['news_list'] = sugg_list
    news_list = News.objects.order_by('-likes')[:15]
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
    sugg_list = get_news_list()
    context_dict['news_list'] = sugg_list
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        user = None
    # Can we find a category with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
    category = Category.objects.get(name__iexact=category_name)
    context_dict['category'] = category
    # Retrieve all of the associated News.
    # Note that filter returns >= 1 model instance.
    news_list = News.objects.filter(category=category).order_by('-rank')
    for news in news_list:
        news.url = encode_url(news.title)
        try:
            news.comments = Comments.objects.filter(news=news).count()
        except Comments.DoesNotExist:
            news.comments = None
        if news.author == user:
            news.like = True
            news.dislike = True
            continue
        # Determine whether user click the like button
        try:
            likes_news = LikeNews.objects.get(user=user, news=news)
            news.like = True
        except LikeNews.DoesNotExist:
            pass
        #Determine whether user click the dislike button
        try:
            dislikes_news = DislikeNews.objects.get(user=user, news=news)
            news.dislike = True
        except DislikeNews.DoesNotExist:
            pass
    # Adds our results list to the template context under name News.
    context_dict['news'] = news_list
    try:
        like_category = LikeCategory.objects.get(user=user, category=category)
        context_dict['like'] = True
    except LikeCategory.DoesNotExist:
        pass
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    # Go render the response and return it to the client.
    return render(request, 'category.html', context_dict)

@login_required
def like_category(request):
    cat_list = []
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()
        user = User.objects.get(username=request.user)
        like_category = LikeCategory(user=user, category=category)
        like_category.save()

def books(request):
    context_dict = {}
    color = ['default', 'primary', 'success', 'info', 'warning', 'danger']
    cat_list = Category.objects.all().order_by('-likes')
    for category in cat_list:
        category.url = encode_url(category.name)
        category.color = choice(color)
    context_dict['cat_list'] = cat_list
    return render(request, 'books.html', context_dict)

def get_books(request, category_name_url):
    category_name = decode_url(category_name_url)
    context_dict = {}
    news_list = get_news_list()
    context_dict['news_list'] = news_list
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        user = None
    # Get the books.
    try:
        category = Category.objects.get(name=category_name)
        books = Book.objects.filter(category=category)
    except:
        context_dict['books'] = None
    for book in books:
        try:
            like_book = LikeBook.objects.get(user=user, book=book)
            book.like = True
        except LikeBook.DoesNotExist:
            pass     
    context_dict['books'] = books
    context_dict['category_name'] = category_name
    return render(request, 'book_list.html', context_dict)

@login_required
def likes_book(request):
    book_id = request.GET['book_id']
    likes = 0
    if book_id:
        book = Book.objects.get(id=int(book_id))
        u = User.objects.get(username=request.user)
        like_book = LikeBook(user=u, book=book)
        like_book.save()
        if book:
            likes = book.likes + 1
            book.likes = likes
            book.save()
        return HttpResponse(likes)

def about(request):
    context_dict = {}
    news_list = get_news_list()
    context_dict['news_list'] = news_list
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    count = request.session.get('visits', 0)
    context_dict['visit_count'] = count
    # Return and render the response, ensuring the count is passed to the template engine.
    return render(request, 'about.html', context_dict)

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
        captcha_form = CaptchaTestForm(request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid() and captcha_form.is_valid():
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
        captcha_form = CaptchaTestForm()
    # Render the template depending on the context.
    return render(
        request, 
        'register.html', 
        {'user_form': user_form, 'profile_form': profile_form, 
        'captcha_form': captcha_form, 'registered': registered})

def user_login(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("Your Startup News account is disabled.")
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if not user:
                user_error = 'User {} does not exit!'.format(username)
                return render(request, 'login.html', {'user_error': user_error})
            else:
                password_error = 'Incorrect password.'
                return render(request, 'login.html', {'password_error': password_error})
            print("Invalid login details: {0}, {1}".format(username, password))   
    else:
        return render(request, 'login.html', {'redirect_to': redirect_to})

@login_required
def user_logout(request):
    redirect_to = request.REQUEST.get('next', '')
    # Use the login_required() decorator to ensure only those logged in can access the view.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(redirect_to)

def password_reset(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'password_reset.html', {})

def user_profile(request, author):
    context_dict = {}
    user = User.objects.get(username=author)
    up = UserProfile.objects.get(user=user)
    try:
        current_user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        current_user = None
    if user == current_user:
        context_dict['reset'] = True
    else:
        views = up.views + 1
        up.views = views
        up.save()
    try:
        news_list = News.objects.filter(author=user)
    except:
        news_list = None
    try:
        comments = Comments.objects.filter(user=user)
        print(comments)
    except:
        comments = None
    context_dict['another_user'] = user
    context_dict['user_profile'] = up
    context_dict['news'] = news_list
    context_dict['comments'] = comments
    return render(request, 'profile.html', context_dict)

@login_required
def profile(request):
    context_dict = {}
    user = User.objects.get(username=request.user)
    context_dict['reset'] = True
    try:
        up = UserProfile.objects.get(user=user)
        up.gender = up.get_gender_display()
    except UserProfile.DoesNotExist:
        up = None
    try:
        news_list = News.objects.filter(author=user)
    except News.DoesNotExist:
        news_list = None
    try:
        comments = Comments.objects.filter(user=user)
    except Comments.DoesNotExist:
        comments = None
    context_dict['another_user'] = user
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
            #news.time = datetime.now().strftime('%Y-%m-%d')
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

@login_required
def likes_news(request):
    news_id = request.GET['news_id']
    if news_id:
        news = News.objects.get(id=int(news_id))
        news_author = news.author
        up = UserProfile.objects.get(user=news_author)
        up.reputation += 1
        up.save()
        # Get the current user
        user = User.objects.get(username=request.user)
        # Save liked news to the database.
        like_news = LikeNews(user=user, news=news)
        like_news.save()
        if news:
            likes = news.likes + 1
            news.likes = likes
            news.save()
        return HttpResponse(likes)

@login_required
def dislikes_news(request):
    news_id = request.GET['news_id']
    if news_id:
        news = News.objects.get(id=int(news_id))
        # Get the current user
        user = User.objects.get(username=request.user)
        # Save disliked news to the database.
        dislike_news = DislikeNews(user=user, news=news)
        dislike_news.save()
        if news:
            dislikes = news.dislikes + 1
            news.dislikes = dislikes
            news.save()
        return HttpResponse(dislikes)

def comments(request, news_title_url):
    context_dict = {}
    news_title = decode_url(news_title_url)
    news = News.objects.get(title=news_title)
    comments = Comments.objects.filter(news=news).order_by('-points')
    context_dict['comments'] = comments
    for comment in comments:
        if comment.user == user:
            for vote_comment in vote_comments:
                if comment.id == vote_comment.commentid:
                    comment.vote = True
                else:
                    comment.vote = False
    context_dict['news_title_url'] = news_title_url
    return render(request, 'comments.html', context_dict)

def add_comment(request, news_id):
    context_dict = {}
    news = News.objects.get(id=news_id)
    if request.method == 'POST':
        comments_form = CommentsForm(data=request.POST)
        if comments_form.is_valid():
            new_comments = comments_form.save(commit=False)
            user = User.objects.get(username=request.user)
            new_comments.user = user
            new_comments.news = news
            # Get the current time and save it to news.time.
            #new_comments.time = datetime.now().strftime('%Y-%m-%d %H:%M')
            # Save the new model instance.
            new_comments.save()
    else:
        comments_form = CommentsForm()
    comments = Comments.objects.filter(news=news).order_by('-points')
    context_dict['comments'] = comments
    try:
        user = User.objects.get(username=request.user)
        vote_comments = VoteComments.objects.filter(user=user)
    except:
        user = None
    for comment in comments:
        if comment.user == user:
            for vote_comment in vote_comments:
                if comment == vote_comment.comment:
                    comment.vote = True
                    break
                else:
                    comment.vote = False
    context_dict['form'] = comments_form
    context_dict['news_id'] = news_id
    return render(request, 'comments.html', context_dict)

@login_required
def vote_comment(request):
    if request.method == 'GET':
        comment_id = int(request.GET['comment_id'])
    if comment_id:
        # Get the current user
        u = User.objects.get(username=request.user)
        # Save liked news to the database.
        vote_comment = VoteComments(user=u, comment_id=comment_id)
        vote_comment.save()
        comment = Comments.objects.get(id=comment_id)
        if comment:
            points = comment.points + 1
            comment.points = points
            comment.save()
        return HttpResponse(points)

@login_required
def auto_add_news(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            u = User.objects.get(username=request.user)
            category = Category.objects.get(id=int(cat_id))
            time = datetime.now().strftime('%Y-%m-%d')
            news = News.objects.get_or_create(category=category, author=u, title=title, url=url, time=time)
            news_list = News.objects.filter(category=category).order_by('-views')
            # Adds our results list to the template context under name news_list.
            context_dict['news_list'] = news_list
    return render(request, 'news_list.html', context_dict)

def reset_password(request):
    context_dict = {}
    if request.method == 'POST':
        form = reset_form(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['newpassword1']
            username = request.user.username
            password = form.cleaned_data['oldpassword']
            user = authenticate(username=username, password=password)
            if user == request.user:
                user.set_password(new_password)
                user.save()
                return render(request, 'reset_password.html', {'reseted': True})
            else:
                return render(request, 'reset_password.html', 
                    {'error':'You have entered wrong old password','form': form})
        else:
            return render(request, 'reset_password.html', 
                {'error':'You have entered old password','form': form})
    else:
        form = reset_form()
    context_dict['form'] = form 
    return render(request, 'reset_password.html', context_dict)

class ResetPasswordRequestView(FormView):
    template_name = "registration/password_reset_email.html"    #code for template is given below the view's code
    success_url = '/share/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
    # This method here validates the if the input is an email address or not. 
    # Its return type is boolean, True if the input is a email address or False if its not.
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
    # A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm). 
        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above
            associated_users= User.objects.filter(email= data)
            # If the input is an valid email address, 
            # then the following code will lookup for users associated with that email address. 
            # If found then an email will be sent to the address, 
            # else an error message will be printed on the screen.
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user.username,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt' 
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'    
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +
                        ". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            # If the input is an username, then the following code will lookup for users associated with that user. 
            # If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'myjita.info',
                        'site_name': 'myjita',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +
                    "'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)