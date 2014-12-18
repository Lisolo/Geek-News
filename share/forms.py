from django import forms
from django.contrib.auth.models import User 
from .models import News, Comments, Tag, UserProfile
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username")
    username.widget.attrs['class'] = 'input-sm form-control'
    email = forms.CharField(help_text="Email")
    email.widget.attrs['class'] = 'form-control'
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    password.widget.attrs['class'] = 'input-sm form-control'
    confirmPassword = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm Password")
    confirmPassword.widget.attrs['class'] = 'input-sm form-control'

    def clean_confirmPassword(self):
        if 'password' in self.cleaned_data and 'confirmPassword' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['confirmPassword']:
                self.add_error('confirmPassword', 'The two password fields did not match.')
                return self
        return self.cleaned_data 

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        )

    website = forms.URLField(help_text="Please enter your website.", required=False)
    website.widget.attrs['class'] = 'input-sm form-control'
    gender = forms.ChoiceField(help_text="Gender", widget=forms.RadioSelect, choices=GENDER)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    picture.widget.attrs['type'] = 'file'

    class Meta:
        model = User
        fields = ('website', 'picture', 'gender',)
    

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()
    captcha.widget.attrs['class'] = 'input-sm form-control'


class TagForm(forms.Form):
    name = forms.CharField(max_length=128, help_text="Please enter the tag name.")
    name.widget.attrs['class'] = 'input-sm form-control'
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the news.")
    title.widget.attrs['class'] = 'form-control'
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the news.")
    url.widget.attrs['class'] = 'form-control'
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
        model = News
        fields = ('title', 'url', 'views',)


class CommentsForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(), label='Enter your comments')
    content.widget.attrs['class'] = 'input-sm form-control'

    class Meta:
        model = Comments
        fields = ('content',)


class reset_form(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput(), help_text='Password')
    oldpassword.widget.attrs['class'] = 'input-sm form-control'
    newpassword1 = forms.CharField(widget=forms.PasswordInput(), help_text='New password')
    newpassword1.widget.attrs['class'] = 'input-sm form-control'
    newpassword2 = forms.CharField(widget=forms.PasswordInput(), help_text='Confirm password')
    newpassword2.widget.attrs['class'] = 'input-sm form-control'

    def clean_newpassword2(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                self.add_error('newpassword2', 'The two password fields didn\'t match.')
                return self
        return self.cleaned_data


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254) 