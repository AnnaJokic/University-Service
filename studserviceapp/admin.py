import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice.settings")


from django.contrib import admin

# Register your models here.

from studserviceapp.models import IzbornaGrupa

admin.site.register(IzbornaGrupa)
