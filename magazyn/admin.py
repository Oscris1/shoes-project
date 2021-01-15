from django.contrib import admin
from .models import Marka, ModelButa, Buty, Sprzedane

# Register your models here.
admin.site.register(Marka)
admin.site.register(ModelButa)
admin.site.register(Buty)
admin.site.register(Sprzedane)