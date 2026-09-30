from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MeView, RegisterView
from . import api_views as api

urlpatterns = [
    path('auth/me/', MeView.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('profile/', api.ProfileView.as_view()),
    path('ingredients/', api.IngredientList.as_view()),
    path('ingredients/<int:pk>/', api.IngredientDetail.as_view()),
    path('meals/', api.MealList.as_view()),
    path('meals/<int:pk>/', api.MealDetail.as_view()),
    path('water/', api.WaterList.as_view()),
    path('water/<int:pk>/', api.WaterDetail.as_view()),
    path('activities/', api.ActivityList.as_view()),
    path('activities/<int:pk>/', api.ActivityDetail.as_view()),
    path('summary/', api.SummaryView.as_view()),
]
