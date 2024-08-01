from django import forms
from .models import Event, Blog, EventData, Comment, Gallery, GalleryItem, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'event_type']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EventDataForm(forms.ModelForm):
    class Meta:
        model = EventData
        fields = ['file', 'file_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['event', 'title', 'description']

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['file', 'is_video', 'title']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']