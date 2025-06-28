from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from rolepermissions.roles import assign_role

from users.models import Admin

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **options):
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        password2 = input('Confirm password: ')

        # todo: properly validate fields

        if password != password2:
            self.stdout.write(self.style.ERROR('Passwords do not match'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('Username already exists'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR('Email already exists'))
            return

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
        )

        Admin.objects.create(user=user)
        assign_role(user, 'admin')

        self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
