from django.contrib.auth.models import AbstractUser

from django.db import models
from datetime import date
from django.utils import timezone

class User(AbstractUser):
    pass

class Person(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "user_person")
    sex = models.CharField(max_length = 10)
    bday = models.DateTimeField()
    height = models.IntegerField()
    weight = models.IntegerField()
    goalweight = models.IntegerField()
    activity = models.IntegerField()
    maintainance = models.IntegerField()
    goalcalorie= models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Food(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "user_food")
    name = models.CharField(max_length = 30)
    grams = models.IntegerField()
    protein = models.IntegerField(default = 0)
    carbs = models.IntegerField(default = 0)
    sodium = models.IntegerField(default = 0)
    cholesterol = models.IntegerField(default = 0)
    sugar = models.IntegerField(default = 0)
    calories = models.IntegerField()
    meal = models.CharField(max_length = 10)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} ate {self.food_tem}"

class Exercise(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "user_exercise")
    exercise = models.CharField(max_length = 30)
    amount = models.IntegerField()
    type = models.CharField(max_length = 10)
    calories = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} did {self.exercise}"