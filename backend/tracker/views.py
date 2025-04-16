from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import timedelta
from rest_framework import generics, views
from .models import UserProfile, PredefinedMeal, CustomMeal, Recipe, IngredientCategory, Ingredient, RecipeIngredient, CalorieEntry, CategoryExercise, Exercise, ExerciseEntry, BurnedCaloriesEntry
from .serializers import UserProfileSerializer, PredefinedMealSerializer, CustomMealSerializer, RecipeSerializer, IngredientCategorySerializer, IngredientSerializer, RecipeIngredientSerializer, CalorieEntrySerializer, ExerciseSerializer, CategoryExerciseSerializer, ExerciseEntrySerializer, BurnedCaloriesEntrySerializer, CaloriesBalanceSerializer, UserSerializer, RegisterSerializer

class UserProfileListCreate(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if UserProfile.objects.filter(user=user).exists():
            raise ValidationError("El usuario ya tiene un perfil creado.")
        serializer.save(user=self.request.user)

class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retorna el perfil del usuario autenticado
        return UserProfile.objects.get(user=self.request.user)



class PredefinedMealListCreate(generics.ListCreateAPIView):
    queryset = PredefinedMeal.objects.all()
    serializer_class = PredefinedMealSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)

class PredefinedMealDetailView(generics.RetrieveAPIView):
    queryset = PredefinedMeal.objects.all()
    serializer_class = PredefinedMealSerializer
    lookup_field = 'id'

class PredefinedMealDeleteView(generics.DestroyAPIView):
    queryset = PredefinedMeal.objects.all()
    serializer_class = PredefinedMealSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Solo permitir eliminar comidas del perfil del usuario autenticado
        user_profile = self.request.user.userprofile
        return PredefinedMeal.objects.filter(user_profile=user_profile)

class PredefinedMealUpdateView(generics.UpdateAPIView):
    queryset = PredefinedMeal.objects.all()
    serializer_class = PredefinedMealSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda editar comidas que pertenecen a su perfil
        user_profile = self.request.user.userprofile
        return PredefinedMeal.objects.filter(user_profile=user_profile)

class PredefinedMealListView(generics.ListAPIView):
    queryset = PredefinedMeal.objects.all()
    serializer_class = PredefinedMealSerializer



class CustomMealListCreate(generics.ListCreateAPIView):
    queryset = CustomMeal.objects.all()
    serializer_class = CustomMealSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)

class CustomMealDetailView(generics.RetrieveAPIView):
    queryset = CustomMeal.objects.all()
    serializer_class = CustomMealSerializer
    lookup_field = 'id'

class CustomMealDeleteView(generics.DestroyAPIView):
    queryset = CustomMeal.objects.all()
    serializer_class = CustomMealSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Solo permitir eliminar comidas del perfil del usuario autenticado
        user_profile = self.request.user.userprofile
        return CustomMeal.objects.filter(user_profile=user_profile)
    
class CustomMealUpdateView(generics.UpdateAPIView):
    queryset = CustomMeal.objects.all()
    serializer_class = CustomMealSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda editar comidas que pertenecen a su perfil
        user_profile = self.request.user.userprofile
        return CustomMeal.objects.filter(user_profile=user_profile)

class CustomMealListView(generics.ListAPIView):
    queryset = CustomMeal.objects.all()
    serializer_class = CustomMealSerializer

    def get_queryset(self):
        # Asegura que solo se muestren las comidas personalizadas asociadas al perfil del usuario
        user_profile = self.request.user.userprofile
        return CustomMeal.objects.filter(user_profile=user_profile) 


class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        # Aquí podrías agregar lógica adicional antes de crear la receta,
        # como asociar la receta con el usuario que la está creando.
        serializer.save(user_profile=self.request.user.userprofile)        

class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # Asegura que solo se muestren las recetas asociadas al perfil del usuario
        user_profile = self.request.user.userprofile
        return Recipe.objects.filter(
            Q(user_profile=user_profile) |
            Q(user_profile__is_creator=True)
        )
    
class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'id'

class RecipeUpdateView(generics.UpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda actualizar recetas pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return Recipe.objects.filter(user_profile=user_profile)
    
    def perform_update(self, serializer):
        # recalcular las calorías totales después de la actualización.
        recipe = serializer.save()
        recipe.total_calories()

class RecipeDeleteView(generics.DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda eliminar recetas pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return Recipe.objects.filter(user_profile=user_profile)
    


class RecipeIngredientCreateView(generics.CreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    def perform_create(self, serializer):
        recipe = self.request.data.get('recipe')
        ingredient = self.request.data.get('ingredient')
        recipe_ingredient = serializer.save(recipe=recipe, ingredient=ingredient)
        recipe_ingredient.recipe.total_calories()  # Recalcular calorías totales de la receta
        
class RecipeIngredientListView(generics.ListAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        recipe_id = self.kwargs['recipe_id']
        # Filtra los ingredientes por receta
        return RecipeIngredient.objects.filter(recipe_id=recipe_id)
    
class RecipeIngredientDeleteView(generics.DestroyAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        recipe = instance.recipe  # Guarda referencia antes de eliminar
        super().perform_destroy(instance)  # Elimina el ingrediente
        recipe.total_calories()  # Recalcula calorías después de eliminar



class IngredientCategoryListCreateView(generics.ListCreateAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer

class IngredientCategoryListView(generics.ListAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer

class IngredientCategoryDetailView(generics.RetrieveAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer
    lookup_field = 'id'

class IngredientCategoryDeleteView(generics.DestroyAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer
    lookup_field = 'id'



class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)

class IngredientListView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        # Asegura que solo se muestren los ingredientes asociados al perfil del usuario
        user_profile = self.request.user.userprofile
        return Ingredient.objects.filter(
            Q(user_profile=user_profile) |
            Q(user_profile__is_creator=True)
        )
    
class IngredientDetailView(generics.RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'

class IngredientUpdateView(generics.UpdateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda actualizar ingredientes pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return Ingredient.objects.filter(user_profile=user_profile)
    
class IngredientDeleteView(generics.DestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda eliminar ingredientes pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return Ingredient.objects.filter(user_profile=user_profile)



class CalorieEntryCreateView(generics.CreateAPIView):
    serializer_class = CalorieEntrySerializer

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile

        # Obtener la comida
        custom_meal = serializer.validated_data.get('custom_meal')
        predefined_meal = serializer.validated_data.get('predefined_meal')
        recipe = serializer.validated_data.get('recipe')
        portion = serializer.validated_data.get('portion', 1)

        # Calcular calorías
        calories = 0
        if custom_meal:
            calories = custom_meal.total_calories * portion
        elif predefined_meal:
            calories = predefined_meal.total_calories * portion
        elif recipe:
            calories = recipe.total_calories * portion
        else:
            calories = serializer.validated_data.get('total_calories', 0) * portion


        serializer.save(user_profile=user_profile, total_calories=calories)

class CalorieEntryListView(generics.ListAPIView):
    serializer_class = CalorieEntrySerializer

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        queryset = CalorieEntry.objects.filter(user_profile=user_profile)

        date_param = self.request.query_params.get('date')
        range_params = self.request.query_params.get('range')

        today = timezone.now().date()

        if date_param:
            # Filtrar por fecha específica
            queryset = queryset.filter(date=date_param)
        elif range_params == 'today':
            # Filtrar por hoy
            queryset = queryset.filter(date=today)
        elif range_params == 'weekly':
            # Filtrar por semana actual
            start_of_week = today - timedelta(days=today.weekday())
            queryset = queryset.filter(date__gte=start_of_week)
        elif range_params == 'monthly':
            # Filtrar por mes actual
            queryset = queryset.filter(date__month=today.month, date__year=today.year)

        return queryset

class CalorieEntryDetailView(generics.RetrieveAPIView):
    serializer_class = CalorieEntrySerializer
    lookup_field = 'id'

    def get_queryset(self):
        return CalorieEntry.objects.filter(user_profile=self.request.user.userprofile)

class CalorieEntryDeleteView(generics.DestroyAPIView):
    serializer_class = CalorieEntrySerializer
    lookup_field = 'id'

    def get_queryset(self):
        return CalorieEntry.objects.filter(user_profile=self.request.user.userprofile)
    


class CategoryExerciseCreateView(generics.ListCreateAPIView):
    queryset = CategoryExercise.objects.all()
    serializer_class = CategoryExerciseSerializer

class CategoryExerciseListView(generics.ListAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = CategoryExerciseSerializer

class CategoryExerciseDeleteView(generics.DestroyAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = CategoryExerciseSerializer
    lookup_field = 'id'



class ExerciseCreateView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def perform_create(self, serializer):
        exercise = serializer.save(user_profile=self.request.user.userprofile)
        exercise.total_calories_burned()  

class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        # Asegura que solo se muestren los ejercicios asociados al perfil del usuario
        user_profile = self.request.user.userprofile
        return Exercise.objects.filter(
            Q(user_profile=user_profile) |
            Q(user_profile__is_creator=True)
        )

class ExerciseDetailView(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'id'

class ExerciseUpdateView(generics.UpdateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda actualizar ejercicios pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return Exercise.objects.filter(user_profile=user_profile)
    
    def perform_update(self, serializer):
        # recalcular las calorías totales después de la actualización.
        exercise = serializer.save()
        exercise.total_calories_burned()  # Recalcular calorías totales del ejercicio

class ExerciseDeleteView(generics.DestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda eliminar ejercicios pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return Exercise.objects.filter(user_profile=user_profile)
    

class ExerciseEntryCreateView(generics.CreateAPIView):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        exercise = serializer.validated_data.get('exercise')
        date = serializer.validated_data.get('date')

        serializer.save(user_profile=user_profile, exercise=exercise, date=date)

class ExerciseEntryListView(generics.ListAPIView):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        queryset = ExerciseEntry.objects.filter(user_profile=user_profile)

        date_param = self.request.query_params.get('date')
        range_params = self.request.query_params.get('range')

        today = timezone.now().date()

        if date_param:
            # Filtrar por fecha específica
            queryset = queryset.filter(date=date_param)
        elif range_params == 'today':
            # Filtrar por hoy
            queryset = queryset.filter(date=today)
        elif range_params == 'weekly':
            # Filtrar por semana actual
            start_of_week = today - timedelta(days=today.weekday())
            queryset = queryset.filter(date__gte=start_of_week)
        elif range_params == 'monthly':
            # Filtrar por mes actual
            queryset = queryset.filter(date__month=today.month, date__year=today.year)

        return queryset
    
class ExerciseEntryDetailView(generics.RetrieveAPIView):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
    lookup_field = 'id'

class ExerciseEntryDeleteView(generics.DestroyAPIView):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda eliminar entradas de ejercicio pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return ExerciseEntry.objects.filter(user_profile=user_profile)
    

class BurnedCaloriesEntryCreateView(generics.CreateAPIView):
    queryset = BurnedCaloriesEntry.objects.all()
    serializer_class = BurnedCaloriesEntrySerializer

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        calories_burned = serializer.validated_data.get('calories_burned')
        name = serializer.validated_data.get('name')
        duration = serializer.validated_data.get('duration')
        date = serializer.validated_data.get('date')

        serializer.save(user_profile=user_profile, calories_burned=calories_burned, name=name, duration=duration, date=date)

class BurnedCaloriesEntryListView(generics.ListAPIView):
    queryset = BurnedCaloriesEntry.objects.all()
    serializer_class = BurnedCaloriesEntrySerializer

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        queryset = BurnedCaloriesEntry.objects.filter(user_profile=user_profile)

        date_param = self.request.query_params.get('date')
        range_params = self.request.query_params.get('range')

        today = timezone.now().date()

        if date_param:
            # Filtrar por fecha específica
            queryset = queryset.filter(date=date_param)
        elif range_params == 'today':
            # Filtrar por hoy
            queryset = queryset.filter(date=today)
        elif range_params == 'weekly':
            # Filtrar por semana actual
            start_of_week = today - timedelta(days=today.weekday())
            queryset = queryset.filter(date__gte=start_of_week)
        elif range_params == 'monthly':
            # Filtrar por mes actual
            queryset = queryset.filter(date__month=today.month, date__year=today.year)

        return queryset
    
class BurnedCaloriesEntryDetailView(generics.RetrieveAPIView):
    queryset = BurnedCaloriesEntry.objects.all()
    serializer_class = BurnedCaloriesEntrySerializer
    lookup_field = 'id'

class BurnedCaloriesEntryDeleteView(generics.DestroyAPIView):
    queryset = BurnedCaloriesEntry.objects.all()
    serializer_class = BurnedCaloriesEntrySerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Asegura que solo pueda eliminar entradas de calorías quemadas pertenecientes a su perfil
        user_profile = self.request.user.userprofile
        return BurnedCaloriesEntry.objects.filter(user_profile=user_profile)
    

class CaloriesBalanceView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CaloriesBalanceSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_profile = request.user.userprofile
        entries_calories = CalorieEntry.objects.filter(user_profile=user_profile)
        entries_burned_calories = BurnedCaloriesEntry.objects.filter(user_profile=user_profile)
        entries_exercise = ExerciseEntry.objects.filter(user_profile=user_profile)

        today = now().date()

        if data.get('range') == 'today':
            entries_calories = entries_calories.filter(date=today)
            entries_burned_calories = entries_burned_calories.filter(date=today)
            entries_exercise = entries_exercise.filter(date=today)
        elif data.get('range') == 'week':
            start = today - timedelta(days=today.weekday())
            entries_calories = entries_calories.filter(date__range=(start, today))
            entries_burned_calories = entries_burned_calories.filter(date__range=(start, today))
            entries_exercise = entries_exercise.filter(date__range=(start, today))
        elif data.get('range') == 'month':
            entries_calories = entries_calories.filter(date__year=today.year, date__month=today.month)
            entries_burned_calories = entries_burned_calories.filter(date__year=today.year, date__month=today.month)
            entries_exercise = entries_exercise.filter(date__year=today.year, date__month=today.month)
        elif data.get('date'):
            entries_calories = entries_calories.filter(date=data['date'])
            entries_burned_calories = entries_burned_calories.filter(date=data['date'])
            entries_exercise = entries_exercise.filter(date=data['date'])

        total_intake = sum(e.total_calories for e in entries_calories)
        total_burned = sum(e.calories_burned for e in entries_burned_calories) + sum(e.exercise.total_calories for e in entries_exercise)

        return Response({
            'total_intake': total_intake,
            'total_burned': total_burned,
            'net_calories': total_intake - total_burned
        })


class MeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
