from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from pages.serializers import RecipeSerializer
from django.core.paginator import Paginator
from django.db.models import Count
import collections

# Create your views here.
from .models import Recipe, Ingredient

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def recipes_list(request):
    recipes = list(Recipe.objects.all().values()[:2000])
    return JsonResponse(recipes, safe=False)

@api_view(['GET'])
def search(request):
    query = request.query_params.getlist('ingredients')
    recipes = list(Recipe.objects.filter(ingredients__name__in=query).annotate(recipe_count=Count('name')).order_by('-recipe_count', '-rating', '-n_ratings').values()[:2000])
    if len(recipes) != 0:
        return JsonResponse(recipes, safe=False)
    else:
        return JsonResponse('error', safe=False, status=404)

@api_view(['GET'])
def find_one(request):
    query = request.query_params.get('recipe') # Name of recipe
    recipe = list(Recipe.objects.filter(id=query).values())
    return JsonResponse(recipe, safe=False) # Need to create new file recipe.html