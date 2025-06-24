from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an admin user (run only via script)'

    def handle(self, *args, **kwargs):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        role = 'admin'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('User already exists'))
            return

        user = User.objects.create_superuser(username=username, email=email, password=password, role=role)

        assign_role(user, 'admin')

        self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
