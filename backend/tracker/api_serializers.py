import math
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from .models import UserProfile, Ingredient, CalorieEntry, MealIngredient, WaterEntry, BurnedCaloriesEntry


class Number(serializers.FloatField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if not math.isfinite(value):
            raise serializers.ValidationError('Introduce un número finito.')
        return value


class Day(serializers.DateField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if value > timezone.localdate() + timezone.timedelta(days=1):
            raise serializers.ValidationError('No se permiten fechas futuras.')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    weight = Number(min_value=1, max_value=600, allow_null=True, required=False)
    height = Number(min_value=30, max_value=300, allow_null=True, required=False)
    goal_weight = Number(min_value=1, max_value=600, allow_null=True, required=False)
    daily_calorie_goal = serializers.IntegerField(min_value=1, max_value=20000, required=False)
    water_goal_ml = serializers.IntegerField(min_value=1, max_value=20000, required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'name', 'weight', 'height', 'goal_weight',
                  'goal', 'daily_calorie_goal', 'water_goal_ml']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    calories = Number(min_value=0, max_value=100000)
    portion_size = Number(min_value=0.01, max_value=100000)
    unit = serializers.ChoiceField(choices=['g', 'ml', 'unidad'])

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'calories', 'portion_size', 'unit']


class MealItemInput(serializers.Serializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.none())
    quantity = Number(min_value=0.01, max_value=100000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['ingredient'].queryset = Ingredient.objects.filter(user_profile__user=request.user)


class MealItemOutput(serializers.ModelSerializer):
    class Meta:
        model = MealIngredient
        fields = ['ingredient', 'name', 'quantity', 'unit', 'calories']


class MealSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='simple_cal_entry', max_length=100)
    date = Day(required=False, default=timezone.localdate)
    calories = Number(source='total_calories', min_value=0, max_value=1000000, required=False)
    ingredients = serializers.ListField(child=serializers.DictField(), write_only=True, required=False, max_length=100)
    items = MealItemOutput(many=True, read_only=True)

    class Meta:
        model = CalorieEntry
        fields = ['id', 'name', 'date', 'calories', 'ingredients', 'items']

    def validate(self, attrs):
        items = attrs.get('ingredients')
        if items is not None:
            parser = MealItemInput(data=items, many=True, context=self.context)
            parser.is_valid(raise_exception=True)
            attrs['ingredients'] = parser.validated_data
        if self.instance and self.instance.items.exists() and items is None and 'total_calories' in attrs:
            raise serializers.ValidationError('Para cambiar las calorías, actualiza los ingredientes o cambia a registro manual.')
        if not items and 'total_calories' not in attrs and (self.instance is None or items == []):
            raise serializers.ValidationError('Añade ingredientes o introduce las calorías manualmente.')
        return attrs

    def save_items(self, meal, items):
        snapshots = []
        for item in items:
            ingredient, quantity = item['ingredient'], item['quantity']
            calories = round(ingredient.calories * quantity / ingredient.portion_size, 2)
            snapshots.append(MealIngredient(meal=meal, ingredient=ingredient, name=ingredient.name,
                                           quantity=quantity, unit=ingredient.unit, calories=calories))
        meal.items.all().delete()
        MealIngredient.objects.bulk_create(snapshots)
        if snapshots:
            meal.total_calories = round(sum(item.calories for item in snapshots), 2)
            meal.save(update_fields=['total_calories'])

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop('ingredients', [])
        validated_data.setdefault('total_calories', 0)
        meal = CalorieEntry.objects.create(**validated_data)
        self.save_items(meal, items)
        return meal

    @transaction.atomic
    def update(self, instance, validated_data):
        items = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)
        if items is not None:
            self.save_items(instance, items)
        return instance


class WaterSerializer(serializers.ModelSerializer):
    amount = Number(min_value=1, max_value=10000)
    date = Day(required=False, default=timezone.localdate)

    class Meta:
        model = WaterEntry
        fields = ['id', 'amount', 'date']


class ActivitySerializer(serializers.ModelSerializer):
    calories_burned = Number(min_value=0, max_value=100000)
    duration = serializers.IntegerField(min_value=1, max_value=1440)
    date = Day(required=False, default=timezone.localdate)

    class Meta:
        model = BurnedCaloriesEntry
        fields = ['id', 'name', 'duration', 'calories_burned', 'date']
