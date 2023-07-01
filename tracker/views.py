import os
import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from datetime import date

from .models import *
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')  
API_URL = 'https://api.api-ninjas.com/v1/nutrition?query='
X_API_URL = 'https://api.api-ninjas.com/v1/caloriesburned?activity='


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register"))
    user = request.user

    person = Person.objects.get(user=user)

    calorie_goal = person.goalcalorie

    foods = Food.objects.filter(user=user, date=date.today())
    total_calorie_gain = 0
    for food in foods:
        total_calorie_gain += food.calories

    exercises = Exercise.objects.filter(user=user, date=date.today())
    total_calorie_burned = 0
    for exercise in exercises:
        total_calorie_burned += exercise.calories

    name = user.first_name

    current_date = date.today()
    person_birthday = person.bday
    age = current_date.year - person_birthday.year

    return render(
        request,
        "tracker/index.html",
        {
            "name": name,
            "calorie_goal": calorie_goal,
            "total_calorie_burned": total_calorie_burned,
            "calories_remaining": calorie_goal - total_calorie_gain,
            "total_calorie_gain": total_calorie_gain,
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "tracker/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["user-name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "tracker/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.save()
        except IntegrityError:
            return render(
                request,
                "tracker/register.html",
                {"message": "Username already taken."},
            )

        sex = request.POST["user-sex"]
        bday = request.POST["user-bday"]
        height = request.POST["user-height"]
        weight = request.POST["user-weight"]
        goalweight = request.POST["user-goalweight"]
        activity = request.POST["user-activity"]

        lvl_activity = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725}

        current_date = date.today()
        person_birthday = bday.split("-")
        age = current_date.year - int(person_birthday[0])

        if sex == "male":
            bmr = 66 + (6.23 * int(weight)) + (12.7 * int(int(height) * 0.394)) - (6.8 * age)
        else:
            bmr = 655 + (4.35 * int(weight)) + (4.7 * int(int(height) * 0.394)) - (4.7 * age)

        maintainance_calories = int(bmr * lvl_activity[activity])

        goal_weight = goalweight
        currentweight = weight
        if goal_weight > currentweight:
            calorie_goal = maintainance_calories + 200
        elif goal_weight < currentweight:
            calorie_goal = maintainance_calories - 200
        else:
            calorie_goal = maintainance_calories

        person = Person(
            user=user,
            sex=sex,
            bday=bday,
            height=height,
            weight=weight,
            goalweight=goalweight,
            activity=activity,
            maintainance=maintainance_calories,
            goalcalorie=calorie_goal,
        )
        person.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "tracker/register.html")


@login_required
def profile(request):
    user = request.user
    person = Person.objects.get(user=user)

    return render(request, "tracker/profile.html", {"person": person})


def edit_profile(request):
    user = request.user
    person = Person.objects.get(user=user)
    if request.method == "POST":
        height = request.POST["height"]
        weight = request.POST["weight"]
        goalweight = request.POST["goalweight"]
        activity = request.POST["activity"]
        goalcalorie = request.POST["goalcalorie"]

        sex = person.sex
        bday = person.bday

        current_date = date.today()
        person_birthday = str(bday).split("-")
        age = current_date.year - int(person_birthday[0])

        lvl_activity = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725, "5": 1.9}

        if sex == "male":
            bmr = 66 + (6.23 * int(weight)) + (12.7 * int(int(height) * 0.394)) - (6.8 * age)
        else:
            bmr = 655 + (4.35 * int(weight)) + (4.7 * int(int(height) * 0.394)) - (4.7 * age)

        maintainance_calories = int(bmr * lvl_activity[activity])

        person.height = height
        person.weight = weight
        person.goalweight = goalweight
        person.activity = activity
        person.goalcalorie = goalcalorie
        person.maintainance = maintainance_calories
        person.save()

    return HttpResponseRedirect(reverse("index"))


@login_required
def food(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        user_ate_today = Food.objects.filter(user=request.user, date=date.today())
        breakfast = user_ate_today.filter(meal="breakfast")
        lunch = user_ate_today.filter(meal="lunch")
        dinner = user_ate_today.filter(meal="dinner")

        total_calories = (
            total_protein
        ) = total_carbs = total_sodium = total_cholesterol = total_sugar = 0

        for food in user_ate_today:
            total_calories += food.calories
            total_protein += food.protein
            total_carbs += food.carbs
            total_sodium += food.sodium
            total_cholesterol += food.cholesterol
            total_sugar += food.sugar

        return render(
            request,
            "tracker/food.html",
            {
                "query": "Enter a valid query",
                "breakfast_food_items": breakfast,
                "lunch_food_items": lunch,
                "dinner_food_items": dinner,
                "total_calories": total_calories,
                "total_protein": total_protein,
                "total_carbs": total_carbs,
                "total_sodium": total_sodium,
                "total_cholesterol": total_cholesterol,
                "total_sugar": total_sugar,
                "today": timezone.now()
            },
        )


@login_required
def addFood(request, meal):
    if not meal:
        return HttpResponse(f"what meal")
    if request.method == "POST":
        food = request.POST["food-name"].lower().strip()
        amount_g = int(request.POST["food-amount"])

        api_request = requests.get(API_URL + food, headers={"X-Api-Key": API_KEY})
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "ERROR"

        serving_size = api[0]["serving_size_g"]

        name = api[0]["name"].capitalize()
        total_calories = amount_g * api[0]["calories"] // serving_size
        protein = api[0]["protein_g"] * amount_g // serving_size
        carbs = api[0]["carbohydrates_total_g"] * amount_g // serving_size
        sodium = api[0]["sodium_mg"] * amount_g // serving_size
        cholesterol = api[0]["cholesterol_mg"] * amount_g // serving_size
        sugar = api[0]["sugar_g"] * amount_g // serving_size
        food_obj = Food(
            user=request.user,
            name=name,
            calories=total_calories,
            grams=amount_g,
            meal=meal,
            protein=protein,
            carbs=carbs,
            sodium=sodium,
            cholesterol=cholesterol,
            sugar=sugar,
        )
        food_obj.save()
        return HttpResponseRedirect(reverse('food'))

    return render(request, "tracker/add-food.html", {"meal": meal})


def get_food_info(request, food_item):
    if request.method == "GET":
        try:
            user = request.user
            food = str(food_item).lower().strip()
            food = food.replace(' ', '+')
            api_request = requests.get(API_URL + food, headers={"X-Api-Key": API_KEY})
            try:
                api = json.loads(api_request.content)
            except Exception as e:
                api = "ERROR"
            food_api = api[0]

            return JsonResponse({"food_api": food_api})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@login_required
def exercise(request):
    total = 0

    cardio = Exercise.objects.filter(user=request.user, date=date.today(), type='cardio')
    strength = Exercise.objects.filter(user=request.user, date=date.today(), type='strength_training')
    other = Exercise.objects.filter(user=request.user, date=date.today(), type='other')
    
    allX = Exercise.objects.filter(user=request.user, date=date.today())
    for x in allX:
        total += x.calories

    return render(request, "tracker/exercise.html", {"cardio_exercises": cardio, "strength_training_exercises": strength, "other_exercises": other, "total_calories_burned": total})


@login_required
def requestExercise(request, exercise):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = int(data.get("minutes"))
        name = data.get("exerciseName")
        type = data.get("exerciseType")
        calories = int(data.get("calories"))
        workout = Exercise(user = request.user, exercise = name, amount = amount, type = type, calories = calories)
        workout.save()
        return JsonResponse({"message": "saved"})
    return render(request, "tracker/add-exercise.html", {"exercise": exercise})


def searchExercise(request, exercise_name, minutes):
    if request.method == "GET":
        try:
            user = request.user
            name = exercise_name
            person = Person.objects.get(user = user)
            weight = str(person.weight)
            api_request = requests.get(X_API_URL + name + "&?&weight=" + weight + "&?&duration=" + str(minutes), headers={"X-Api-Key": API_KEY})
            try:
                api = json.loads(api_request.content)
            except Exception as e:
                api = "ERROR"
            x_api = api

            return JsonResponse({"x_api": x_api})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def addExercise(request, exercise_name):
    if request.method == "POST":
        try:
            # create the exercise
            data = json.loads(request.body)
            if data.get("content") is not None:
                amount = data["minutes"]

            person = Person.objects.get(user=request.user)
            weight = person.weight

            # use the api to calculate the calories
            name = exercise_name.replace(' ', '+')
            api_request = requests.get(X_API_URL + name + "?weight" + weight + "?duration" + amount, headers={"X-Api-Key": API_KEY})
            try:
                api = json.loads(api_request.content)
            except Exception as e:
                api = "ERROR"
            x_api = api[0]

            exercise_obj = Exercise(
                user=request.user, exercise=exercise, amount=amount, calories=calories
            )
            exercise_obj.save()

            return JsonResponse(
                {
                    "message": "Exercise added successfully."
                }
            )
        except:
            return JsonResponse({"error": "Like not found."}, status=404)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'tracker/change_password.html', {'form': form})