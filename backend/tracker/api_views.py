from django.utils import timezone
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from .models import Ingredient, CalorieEntry, WaterEntry, BurnedCaloriesEntry
from .api_serializers import ProfileSerializer, IngredientSerializer, MealSerializer, WaterSerializer, ActivitySerializer
from .services import profile_for, daily_summary


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


def requested_day(request):
    raw = request.query_params.get('date')
    return serializers.DateField().run_validation(raw) if raw else timezone.localdate()


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return profile_for(self.request.user)


class OwnedQueryset:
    """Every read and write is scoped to the authenticated owner."""
    pagination_class = Pagination
    dated = False

    def get_queryset(self):
        queryset = self.queryset.filter(user_profile__user=self.request.user)
        if self.dated:
            queryset = queryset.filter(date=requested_day(self.request)) if 'date' in self.request.query_params else queryset
            return queryset.order_by('-date', '-id')
        return queryset.order_by('name', 'id')

    def perform_create(self, serializer):
        serializer.save(user_profile=profile_for(self.request.user))


class IngredientList(OwnedQueryset, generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientDetail(OwnedQueryset, generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class MealList(OwnedQueryset, generics.ListCreateAPIView):
    queryset = CalorieEntry.objects.prefetch_related('items')
    serializer_class = MealSerializer
    dated = True


class MealDetail(OwnedQueryset, generics.RetrieveUpdateDestroyAPIView):
    queryset = CalorieEntry.objects.prefetch_related('items')
    serializer_class = MealSerializer
    dated = True


class WaterList(OwnedQueryset, generics.ListCreateAPIView):
    queryset = WaterEntry.objects.all()
    serializer_class = WaterSerializer
    dated = True


class WaterDetail(OwnedQueryset, generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterEntry.objects.all()
    serializer_class = WaterSerializer
    dated = True


class ActivityList(OwnedQueryset, generics.ListCreateAPIView):
    queryset = BurnedCaloriesEntry.objects.all()
    serializer_class = ActivitySerializer
    dated = True


class ActivityDetail(OwnedQueryset, generics.RetrieveUpdateDestroyAPIView):
    queryset = BurnedCaloriesEntry.objects.all()
    serializer_class = ActivitySerializer
    dated = True


class SummaryView(views.APIView):
    def get(self, request):
        return Response(daily_summary(profile_for(request.user), requested_day(request)))
