from django.contrib import admin
from .models import Category, Photo, ShortnerURL, Like, PhotoComment
# Register your models here.

admin.site.register(Category)
admin.site.register((Photo, PhotoComment))
admin.site.register(ShortnerURL)
admin.site.register(Like)