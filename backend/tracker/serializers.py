from rest_framework import serializers
from .models import UserProfile, PredefinedMeal, CustomMeal, IngredientCategory, Ingredient, Recipe, RecipeIngredient, CalorieEntry, Exercise, CategoryExercise, ExerciseEntry, BurnedCaloriesEntry

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class PredefinedMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedMeal
        fields = '__all__'

class CustomMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMeal
        fields = '__all__'

class IngredientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientCategory
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    category = IngredientCategorySerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'



class CalorieEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalorieEntry
        fields = '__all__'
        read_only_fields = ['user_profile','date']



class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class CategoryExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExercise
        fields = '__all__'

class ExerciseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseEntry
        fields = '__all__'

class BurnedCaloriesEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BurnedCaloriesEntry
        fields = '__all__'


class CaloriesBalanceSerializer(serializers.Serializer):
    range = serializers.ChoiceField(choices=['today', 'week', 'month'], required=False)
    date = serializers.DateField(required=False)

    def validate(self, data):
        if not data.get('range') and not data.get('date'):
            raise serializers.ValidationError("Debes especificar un rango ('range') o una fecha específica ('date').")
        return data