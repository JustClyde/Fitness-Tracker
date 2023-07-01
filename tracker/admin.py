from django.contrib import admin
from .models import User, Person, Food, Exercise

# Register your models here.
admin.site.register(User)
admin.site.register(Person)
admin.site.register(Food)
admin.site.register(Exercise)
