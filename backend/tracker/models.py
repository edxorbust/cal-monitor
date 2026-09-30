from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # Relacionamos con el usuario
    image_url = models.URLField(max_length=500, blank=True, null=True)  # URL de la imagen del perfil
    is_creator = models.BooleanField(default=False)
    #Información de usuario
    name= models.CharField(max_length=100, blank=True)
    lastname= models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender_choices = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'No binario'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)
    notes = models.TextField(blank=True)

    #Historial Clinico
    reason_of_consult = models.TextField(blank=True)
    blood_type_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_type = models.CharField(max_length=3, choices=blood_type_choices, blank=True)
    surgeries = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    previous_diagnoses = models.TextField(blank=True)
    previous_treatments = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    hashtag = models.CharField(max_length=100, blank=True)

    #Información de estilo de vida
    #work
    work_type = models.TextField(blank=True)
    description_work = models.TextField(blank=True)
    work_hours = models.PositiveIntegerField(null=True, blank=True)
    stress_level = [
        ('0', 'Ninguno'),
        ('1', 'Ocasional'),
        ('2', 'Repetitivo'),
        ('3', 'Crónico'),
    ]
    stress_level = models.CharField(max_length=1, choices=stress_level, blank=True)

    #physical activity
    physical_activity = models.TextField(blank=True)

    #diet habits
    unliked_foods = models.TextField(blank=True)
    liked_foods = models.TextField(blank=True)
    breakfast = models.TextField(blank=True)
    lunch = models.TextField(blank=True)
    dinner = models.TextField(blank=True)
    
    #toxic habits
    smoking_frecuency = [
        ('no','No'),
        ('ex','Ex fumador'),
        ('month','Mensual'),
        ('2month','2 veces al mes'),
        ('3month','3 veces al mes'),
        ('week','Semanal'),
        ('2week','2 veces a la semana'),
        ('3week','3 veces a la semana'),
        ('4week','4 veces a la semana'),
        ('5week','5 veces a la semana'),
        ('6week','6 veces a la semana'),
        ('daily','Diario'),
    ]
    smoking_frecuency = models.CharField(max_length=25, choices=smoking_frecuency, blank=True)
    smoking_quantity = models.PositiveIntegerField(null=True, blank=True)
    alcohol_frecuency = [
       ('no','No'),
        ('ex','Ex bebedor'),
        ('month','Mensual'),
        ('2month','2 veces al mes'),
        ('3month','3 veces al mes'),
        ('week','Semanal'),
        ('2week','2 veces a la semana'),
        ('3week','3 veces a la semana'),
        ('4week','4 veces a la semana'),
        ('5week','5 veces a la semana'),
        ('6week','6 veces a la semana'),
        ('daily','Diario'),
    ]
    alcohol_frecuency = models.CharField(max_length=25, choices=alcohol_frecuency, blank=True)
    alcohol_quantity = models.PositiveIntegerField(null=True, blank=True)
    drug_frecuency = [
       ('no','No'),
        ('ex','Ex consumidor'),
        ('month','Mensual'),
        ('2month','2 veces al mes'),
        ('3month','3 veces al mes'),
        ('week','Semanal'),
        ('2week','2 veces a la semana'),
        ('3week','3 veces a la semana'),
        ('4week','4 veces a la semana'),
        ('5week','5 veces a la semana'),
        ('6week','6 veces a la semana'),
        ('daily','Diario'),
    ]
    drug_frecuency = models.CharField(max_length=25, choices=drug_frecuency, blank=True)
    drug_quantity = models.PositiveIntegerField(null=True, blank=True)

    #Información de salud
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    activity_level_choices = [
        ('1', 'Sedentario'),
        ('2', 'Ligeramente activo'),
        ('3', 'Moderadamente activo'),
        ('4', 'Altamente activo'),
        ('5', 'Atleta'),
    ]
    activity_level = models.CharField(max_length=1, choices=activity_level_choices, blank=True)
    goal_choices = [
        ('P', 'Perder peso'),
        ('G', 'Ganar peso'),
        ('M', 'Mantener peso'),
    ]
    goal = models.CharField(max_length=1, choices=goal_choices, blank=True)
    strategy = models.TextField(blank=True)


    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    water_goal_ml = models.PositiveIntegerField(default=2000)
    goal_weight = models.FloatField(null=True, blank=True)

    def get_daily_calories(self):
        today = timezone.now().date()
        return sum(entry.total_calories for entry in self.calorieentry_set.filter(date=today))

    def get_weekly_calories(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        return sum(entry.total_calories for entry in self.calorieentry_set.filter(date__gte=start_of_week))

    def get_monthly_calories(self):
        today = timezone.now().date()
        return sum(entry.total_calories for entry in self.calorieentry_set.filter(date__month=today.month))

class PredefinedMeal(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='predefined_meals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    calories = models.IntegerField()
    carbs_serving = models.FloatField()  # Ración de hidratos de carbono
    habit_measurement_description = models.CharField(max_length=255)  # Ejemplo: "unidad", "taza"
    habit_measurement_value = models.FloatField()  # Ejemplo: 110
    habit_measurement_unit = models.CharField(max_length=10)  # Ejemplo: "gr", "ml"
    carbs_per_serving_grams = models.FloatField()  # Cantidad de 1 ración de hidratos de carbono en gramos

    def __str__(self):
        return self.name
    
class CustomMeal(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='custom_meals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    portion = models.FloatField()  # Porción de la comida, por ejemplo: 200
    unit = models.CharField(max_length=10)  # Unidad de medida, por ejemplo: "gr" o "ml"
    total_carbs = models.FloatField()  # Total de carbohidratos en gramos, por ejemplo: 800

    def __str__(self):
        return self.name
    
class IngredientCategory(models.Model):
    name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=255, blank=True, null=True)  # Ruta de la imagen de la categoría
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='ingredient', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True, blank=True)
    calories = models.FloatField()
    unit = models.CharField(max_length=10)  # Ejemplo: "gr", "ml"
    portion_size = models.FloatField()  # Tamaño de la porción en gramos o mililitros
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='recipe', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    calories = models.FloatField(default=0.0)
    instructions = models.TextField(blank=True, null=True)
    portions = models.IntegerField(default=1)  # Número de porciones que rinde la receta
    preparation_time = models.IntegerField(default=0)  # Tiempo de preparación en minutos
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def total_calories(self):
        total = 0.0
        for ingredient in self.ingredients.all():
            total += ingredient.calories
        return total

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    portion = models.FloatField()
    calories = models.FloatField(default=0.0)  # Calorías de la porción del ingrediente en la receta

    def total_calories(self):
        self.calories = (self.portion * self.ingredient.calories) / self.ingredient.portion_size
        self.save()
    
    def __str__(self):
        return self.name
    
class CalorieEntry(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    
    # Uno de estos será usado según lo que se haya consumido
    custom_meal = models.ForeignKey('CustomMeal', null=True, blank=True, on_delete=models.SET_NULL)
    predefined_meal = models.ForeignKey('PredefinedMeal', null=True, blank=True, on_delete=models.SET_NULL)
    recipe = models.ForeignKey('Recipe', null=True, blank=True, on_delete=models.SET_NULL)
    simple_cal_entry = models.CharField(max_length=100, null=True, blank=True) 
    
    portion = models.FloatField(null=True, blank=True)  # Porción consumida en unidad de la comida
    total_calories = models.FloatField()  # Calorías resultantes de esa porción
    
    date = models.DateField(default=timezone.localdate, db_index=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.date} - {self.total_calories} kcal"



class CategoryExercise(models.Model):
    name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=255, blank=True, null=True)  # Ruta de la imagen de la categoría

    def __str__(self):
        return self.name

class Exercise(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='exercise', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    duration = models.IntegerField()  # Duración del ejercicio en minutos
    category = models.ForeignKey(CategoryExercise, on_delete=models.CASCADE)
    total_calories = models.FloatField(default=0.0)  # Calorías totales quemadas en la sesión de ejercicio

    def __str__(self):
        return self.name
    
class ExerciseEntry(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate, db_index=True)
    duration = models.IntegerField(null=True, blank=True)  # Duración del ejercicio en minutos
    total_calories = models.FloatField(null=True, blank=True)  # Calorías quemadas en la sesión de ejercicio

    def save(self, *args, **kwargs):
        if self.exercise:
            if self.duration is None:
                self.duration = self.exercise.duration
                self.total_calories = self.exercise.total_calories
            else:
                self.total_calories = (self.exercise.total_calories * self.duration)/self.exercise.duration
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.exercise.name} - {self.date}"
    
class BurnedCaloriesEntry(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Nombre del ejercicio
    calories_burned = models.FloatField()  # Calorías quemadas en la sesión de ejercicio
    duration = models.IntegerField()  # Duración del ejercicio en minutos
    date = models.DateField(default=timezone.localdate, db_index=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.name} - {self.calories_burned} kcal - {self.date}"
    

class WaterEntry(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.FloatField()  # Cantidad de agua consumida en mililitros
    date = models.DateField(default=timezone.localdate, db_index=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.amount} ml - {self.date}"

class MealIngredient(models.Model):
    """Snapshot of an ingredient portion; historical meals survive catalog edits."""
    meal = models.ForeignKey(CalorieEntry, related_name='items', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)
    calories = models.FloatField()
