from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Profile

class Command(BaseCommand):
    help = 'Creates user profiles for existing users'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            Profile.create_profile(user)
        self.stdout.write(self.style.SUCCESS('Successfully created user profiles'))