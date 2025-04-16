from django.contrib import admin
from .models import UserProfile, PredefinedMeal, CustomMeal, IngredientCategory, Ingredient, Recipe, RecipeIngredient, CalorieEntry, Exercise, CategoryExercise, ExerciseEntry, BurnedCaloriesEntry
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PredefinedMeal)
admin.site.register(CustomMeal)
admin.site.register(IngredientCategory)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(CalorieEntry)
admin.site.register(Exercise)
admin.site.register(CategoryExercise)
admin.site.register(ExerciseEntry)
admin.site.register(BurnedCaloriesEntry)
