from django.contrib import admin
from .models import User, UserQouta, Reset

# Register your models here.
admin.site.register(User)
admin.site.register(UserQouta)
admin.site.register(Reset)
