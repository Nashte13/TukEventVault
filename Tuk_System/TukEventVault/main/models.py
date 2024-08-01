from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    event_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class EventData(models.Model):
    event = models.ForeignKey(Event, related_name='data', on_delete=models.CASCADE)
    file = models.FileField(upload_to='event_data/')
    file_type = models.CharField(max_length=20, choices=[
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.event.title} - {self.file_type}"
    
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.event.title}'

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'


class Gallery(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} Gallery"

class GalleryItem(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='items', on_delete=models.CASCADE)
    file = models.FileField(upload_to='gallery/')
    is_video = models.BooleanField(default=False)
    title = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Video' if self.is_video else 'Image'} for {self.gallery.event.title}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional user fields as needed
    
    def __str__(self):
        return self.user.username
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.profile_picture:
            img = Image.open(self.profile_picture)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img_file = io.BytesIO()
                img.save(img_file, format='JPEG', quality=85)
                file_name = self.profile_picture.name
                self.profile_picture = InMemoryUploadedFile(
                    img_file,
                    None,
                    file_name,
                    'image/jpeg',
                    img_file.tell,
                    None
                )
        super().save(*args, **kwargs)

    @classmethod
    def create_profile(cls, user):
        return cls.objects.get_or_create(user=user)[0]

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.create_profile(instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()