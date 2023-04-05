from django.contrib import admin

from .models import Projects, CoverLetter, Skills

# Register your models here.
admin.site.register(Projects)
admin.site.register(CoverLetter)
admin.site.register(Skills)
