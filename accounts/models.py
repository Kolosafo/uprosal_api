from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import datetime, timezone
from .managers import UserManager
today = datetime.now(timezone.utc)

# Create your models here.


categories = (
    ('Accounting and Consulting', 'Accounting and Consulting'),
    ('Admin Support', 'Admin Support'),
    ('Customer Service', 'Customer Service'),
    ('Data Science and Analysis', 'Data Science and Analysis'),
    ('Design and Creative', 'Design and Creative'),
    ('Engineering and Architecture', 'Engineering and Architecture'),
    ('IT & Networking', 'IT & Networking'),
    ('Legal', 'Legal'),
    ('Sales and Marketing', 'Sales and Marketing'),
    ('Translation', 'Translation'),
    ('Web, Mobile, & Software Development', 'Web, Mobile, & Software Development'),
    ('Writing', 'Writing'),
)


account_status = (
    ("Not Activated", "Not Activated"),
    ("Trial", "Trial"),
    ("Trial Ended", "Trial Ended"),
    ("Paid", "Paid"),
    ("Subscription Expired", "Subscription Expired"),
)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=today, blank=True)
    work_category = models.CharField(
        max_length=255, choices=categories, blank=True)

    status = models.CharField(
        max_length=20, choices=account_status, blank=False, default="Not Activated")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_created=True, blank=True, null=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        token = str(self.token)
        return token


class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email
