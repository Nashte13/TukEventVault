from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event, Blog
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import EventForm, EventData, EventDataForm
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import modelformset_factory
from django.db.models import Q
from django.http import FileResponse
from django.contrib.auth.models import User
from .forms import CommentForm, BlogForm, GalleryForm, GalleryItemForm, CustomUserCreationForm, ProfileForm, Profile
from .models import Comment, Gallery, GalleryItem
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

def home(request):
    events = Event.objects.all().order_by('-date')[:5]
    blogs = Blog.objects.all().order_by('-created_at')[:5]
    return render(request, 'main/home.html', {'events': events, 'blogs': blogs})

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'main/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_data = EventData.objects.filter(event=event)
    comments = Comment.objects.filter(event=event).order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            new_comment = comment_form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()
            return redirect('event_detail', event_id=event.id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'main/event_detail.html', {
        'event': event,
        'event_data': event_data,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def user_dashboard(request):
    return render(request, 'main/user_dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        return render(request, 'main/admin_dashboard.html')
    else:
        return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


#creating and editting events
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_event(request):
    EventDataFormSet = modelformset_factory(EventData, form=EventDataForm, extra=1)

    if request.method == 'POST':
        event_form = EventForm(request.POST)
        formset = EventDataFormSet(request.POST, request.FILES, queryset=EventData.objects.none())
        
        if event_form.is_valid() and formset.is_valid():
            event = event_form.save()
            for form in formset:
                if form.cleaned_data:
                    event_data = form.save(commit=False)
                    event_data.event = event
                    event_data.save()
            return redirect('event_detail', event_id=event.id)
    else:
        event_form = EventForm()
        formset = EventDataFormSet(queryset=EventData.objects.none())
    
    return render(request, 'main/add_event.html', {'event_form': event_form, 'formset': formset})

@login_required
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'main/event_form.html', {'form': form, 'event': event})

#Blogs
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'main/blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.user = request.user
            new_comment.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        comment_form = CommentForm()

    return render(request, 'main/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = BlogForm()
    return render(request, 'main/blog_form.html', {'form': form})

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user != blog.author:
        return redirect('blog_list')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'main/blog_form.html', {'form': form, 'blog': blog})

#uploading event data
@login_required
def upload_event_data(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventDataForm(request.POST, request.FILES)
        if form.is_valid():
            event_data = form.save(commit=False)
            event_data.event = event
            event_data.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventDataForm()
    return render(request, 'main/upload_event_data.html', {'form': form, 'event': event})

@staff_member_required
def admin_dashboard(request):
    users = User.objects.all()
    events = Event.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'main/admin_dashboard.html', {
        'users': users,
        'events': events,
        'blogs': blogs
    })

#Gallery views
def gallery_list(request):
    events = Event.objects.filter(gallery__isnull=False).distinct()
    return render(request, 'main/gallery_list.html', {'events': events})

def gallery_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    gallery = get_object_or_404(Gallery, event=event)
    items = gallery.items.all()
    return render(request, 'main/gallery_detail.html', {'event': event, 'gallery': gallery, 'items': items})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_gallery(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.event = event
            gallery.save()
            return redirect('gallery_detail', event_id=event.id)
    else:
        form = GalleryForm(initial={'event': event})
    return render(request, 'main/gallery_form.html', {'form': form, 'event': event})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_gallery_item(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.gallery = gallery
            item.save()
            return redirect('gallery_detail', event_id=gallery.event.id)
    else:
        form = GalleryItemForm()
    return render(request, 'main/gallery_item_form.html', {'form': form, 'gallery': gallery})

@login_required
def download_gallery_item(request, item_id):
    item = get_object_or_404(GalleryItem, id=item_id)
    return FileResponse(item.file, as_attachment=True)

#search view
def search_view(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        blogs = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        events = Event.objects.none()
        blogs = Blog.objects.none()
    
    context = {
        'query': query,
        'events': events,
        'blogs': blogs,
    }
    return render(request, 'main/search_results.html', context)

#sharing and download features for logged in users
@login_required
def download_event_data(request, event_data_id):
    event_data = EventData.objects.get(id=event_data_id)
    return FileResponse(event_data.file, as_attachment=True)


#user management views
@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'main/user_list.html', {'users': users})

@staff_member_required
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'main/user_detail.html', {'user': user})

@staff_member_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        return redirect('user_detail', user_id=user.id)
    return render(request, 'main/edit_user.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password.')
    return render(request, 'main/login.html')
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'main/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'main/edit_profile.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, let's just print the data
        print(f"Received message from {name} ({email}): {subject} - {message}")
        
        # Add a success message
        messages.success(request, 'Your message has been sent. We will get back to you soon!')
        
        # Redirect back to the contact page
        return redirect('contact')
    
    return render(request, 'main/contact.html')

def faq(request):
    return render(request, 'main/faq.html')

def event_submission(request):
    return render(request, 'main/event_submission.html')

def report_issue(request):
    return render(request, 'main/report_issue.html')