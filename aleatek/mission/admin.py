from django.contrib import admin

# Register your models here.
from .models import Mission, Article

admin.site.register(Mission)
admin.site.register(Article)

