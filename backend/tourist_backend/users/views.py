from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer
import os
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({"error": "Invalid username or password"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        })
import requests
from django.http import JsonResponse
from django.conf import settings
import requests
from django.http import JsonResponse
from django.conf import settings

import requests
from django.http import JsonResponse
from django.conf import settings

def get_city_coordinates(city):  # This should accept only city
    OPENCAGE_API_KEY = settings.OPENCAGE_API_KEY
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city},India&key={OPENCAGE_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["results"]:
            lat = data["results"][0]["geometry"]["lat"]
            lon = data["results"][0]["geometry"]["lng"]
            return lat, lon
        else:
            return None, None
    except requests.RequestException as e:
        return None, None


def get_nearby_tourist_places(request):
    """Fetch tourist places and their images using HERE API"""
    state = request.GET.get("state")
    city = request.GET.get("city")
    limit = request.GET.get("limit", 50)  # Default: 50 places

    if not state or not city:
        return JsonResponse({"error": "State and City are required"}, status=400)

    # Get city coordinates
    latitude, longitude = get_city_coordinates( city)
    if not latitude or not longitude:
        return JsonResponse({"error": "Invalid state or city"}, status=400)

    HERE_API_KEY = settings.HERE_API_KEY
    here_url = f"https://discover.search.hereapi.com/v1/discover?at={latitude},{longitude}&limit={limit}&q=attraction&apiKey={HERE_API_KEY}"

    try:
        here_response = requests.get(here_url)
        here_response.raise_for_status()
        here_data = here_response.json()
    except requests.RequestException as e:
        print(f"Error fetching tourist places: {e}")
        return JsonResponse({"error": "Failed to fetch places from HERE API"}, status=500)

    places = []
    
    for item in here_data.get("items", []):
        place_name = item["title"]
        address = item.get("address", {}).get("label", "Unknown Address")
        lat = item["position"]["lat"]
        lon = item["position"]["lng"]
        place_id = item["id"]  # HERE Place ID

        # Fetch images using HERE API
        image_urls = fetch_here_place_images(place_id)

        places.append({
            "name": place_name,
            "address": address,
            "latitude": lat,
            "longitude": lon,
            "image_urls": image_urls
        })

    return JsonResponse({"places": places})


def fetch_here_place_images(place_id):
    """Fetch images for a place using HERE API"""
    HERE_API_KEY = settings.HERE_API_KEY
    image_url = f"https://browse.search.hereapi.com/v1/browse/{place_id}/photos?apiKey={HERE_API_KEY}"

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        data = response.json()

        if "items" not in data:
            return []

        image_urls = [img["href"] for img in data["items"]]
        return image_urls if image_urls else ["https://via.placeholder.com/300"]

    except requests.RequestException as e:
        print(f"Error fetching images: {e}")
        return []
