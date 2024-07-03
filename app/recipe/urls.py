"""
URL mapping for the recipe API.
"""

from django.urls import path, include # define apath and include url bzy url name
from rest_framework.routers import DefaultRouter # use with api to automatically create routs for all the option

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]