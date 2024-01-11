from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import redis
import json
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
from django.conf import settings

url = "https://the-vegan-recipes-db.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": settings.API_KEY,
	"X-RapidAPI-Host": settings.API_DOMAIN
}

DUMMY_DATA = '{ "test": "test" }'

@api_view(['GET'])
def getRecipes (req): 
    data = r.get('recipes')

    if (data != None):
        return Response(json.loads(data))

    freshData = requests.get(url, headers=headers).json()
    r.set('recipes', json.dumps(freshData))
    return Response(freshData)

@api_view(['GET'])
def getRecipeById (req, id):
    recipe_id = int(id)

    if recipe_id <= 0:
        recipe_id = 0

    data = r.get(recipe_id)

    if (data != None):
        return Response(json.loads(data))
    
    freshData = requests.get(f'{url}{recipe_id}', headers=headers).json()
    r.set(id, json.dumps(freshData))
    return Response(freshData)
