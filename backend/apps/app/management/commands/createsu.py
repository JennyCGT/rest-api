from django.core.management.base import BaseCommand
from apps.authentication.models import User
     

class Command(BaseCommand):
  def handle(self, *args, **options):
      if not User.objects.filter(email="admin@gmail.com").exists(): #change email for username if you user django User model
        User.objects.create_superuser( "admin@gmail.com", "admin") # email/username and the password