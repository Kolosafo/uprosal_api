from django.db import models

# Create your models here.


class Projects(models.Model):
    user = models.EmailField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=455)
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user


class CoverLetter(models.Model):
    user = models.EmailField(max_length=255, null=True)
    letter = models.CharField(max_length=10000)

    def __str__(self):
        return self.user
