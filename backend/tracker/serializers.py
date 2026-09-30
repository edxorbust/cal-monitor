from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import UserProfile, PredefinedMeal, CustomMeal, IngredientCategory, Ingredient, Recipe, RecipeIngredient, CalorieEntry, Exercise, CategoryExercise, ExerciseEntry, BurnedCaloriesEntry, WaterEntry

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']

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
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        try:
            validate_password(data['password'], User(username=data['username'], email=data.get('email', '')))
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': list(exc.messages)})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # ya no se necesita
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user, name=user.username, email=user.email)
        return user
    
class WaterEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterEntry
        fields = '__all__'
        read_only_fields = ['user_profile','date']
