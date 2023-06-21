from django.contrib import admin

# Register your models here.
from .models import Ouvrage, Documents, Aso

admin.site.register(Ouvrage)
admin.site.register(Documents)
admin.site.register(Aso)