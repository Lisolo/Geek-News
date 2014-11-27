from django import forms

from django.contrib.auth.models import User 

from .models import News, Comments, Category, UserProfile

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username")
    username.widget.attrs['class'] = 'input-sm form-control'

    email = forms.CharField(help_text="Email")
    email.widget.attrs['class'] = 'form-control'

    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    password.widget.attrs['class'] = 'input-sm form-control'

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        )

    website = forms.URLField(help_text="Please enter your website.", required=False)
    website.widget.attrs['class'] = 'input-sm form-control'

    gender = forms.ChoiceField(help_text="Gender", widget=forms.RadioSelect, choices=GENDER)

    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    
    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'gender',) 

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category

class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the news.")
    title.widget.attrs['class'] = 'form-control'

    url = forms.URLField(max_length=200, help_text="Please enter the URL of the news.")
    url.widget.attrs['class'] = 'input-sm form-control'

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = News

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('title', 'url', 'views',)        

class CommentsForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(), label='Enter your comments')
    content.widget.attrs['class'] = 'input-sm form-control'

    class Meta:
        model = Comments
        fields = ('content',)   