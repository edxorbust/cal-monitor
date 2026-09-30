from django.db.models import Sum
from .models import UserProfile, CalorieEntry, BurnedCaloriesEntry, ExerciseEntry, WaterEntry


def profile_for(user):
    return UserProfile.objects.get_or_create(
        user=user, defaults={'name': user.username, 'email': user.email}
    )[0]


def daily_summary(profile, day):
    def total(model, field):
        return model.objects.filter(user_profile=profile, date=day).aggregate(value=Sum(field))['value'] or 0

    consumed = total(CalorieEntry, 'total_calories')
    burned = total(BurnedCaloriesEntry, 'calories_burned') + total(ExerciseEntry, 'total_calories')
    water = total(WaterEntry, 'amount')
    return {
        'date': day, 'consumed': round(consumed, 2), 'burned': round(burned, 2),
        'net': round(consumed - burned, 2),
        'remaining': round(profile.daily_calorie_goal - consumed + burned, 2),
        'calorie_goal': profile.daily_calorie_goal, 'water_ml': water,
        'water_goal_ml': profile.water_goal_ml,
        'meal_count': CalorieEntry.objects.filter(user_profile=profile, date=day).count(),
    }
