from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer,VisitSerializer
from .models import Visit
from rest_framework.permissions import IsAuthenticated


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
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view


GOOGLE_PLACES_API_KEY = settings.API_KEY

@api_view(['GET'])
def get_tourist_places(request):
    place_name = request.GET.get("place_name", "")
    print(f"Received request for place: {place_name}")

    if not place_name:
        print("Error: Missing place name")
        return Response({"error": "Missing place name"}, status=400)

    google_url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query={place_name}&key={GOOGLE_PLACES_API_KEY}"
    )

    print(f"Requesting Google Places API: {google_url}")

    try:
        response = requests.get(google_url)
        data = response.json()

        print("Google API Raw Response:", data)

        if "error_message" in data:
            print("Google API Error:", data["error_message"])
            return Response({"error": data["error_message"]}, status=400)

        if "results" in data:
            places = []
            for place in data["results"]:
                place_info = {
                    "place_id": place.get("place_id", ""),  # Added place_id
                    "name": place.get("name", "Unknown Place"),
                    "address": place.get("formatted_address", "Address Not Available"),
                    "photo_url": None  # Default None if no photo found
                }

                # Check if photos exist
                if "photos" in place and len(place["photos"]) > 0:
                    photo_reference = place["photos"][0]["photo_reference"]
                    place_info["photo_url"] = (
                        f"https://maps.googleapis.com/maps/api/place/photo?"
                        f"maxwidth=400&photo_reference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
                    )

                places.append(place_info)

            print(f"Returning {len(places)} places.")
            return Response({"places": places})
        else:
            print("No places found in API response.")
            return Response({"error": "No places found"}, status=404)

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response({"error": str(e)}, status=500)


class VisitCreateView(generics.CreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VisitListView(generics.ListAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        place_id = self.kwargs['place_id']
        return Visit.objects.filter(place_id=place_id)

def get_place_details(request):
    place_id = request.GET.get("place_id")
    if not place_id:
        return JsonResponse({"error": "Missing place_id"}, status=400)

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_PLACES_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "result" not in data:
        return JsonResponse({"error": "Invalid place_id"}, status=404)

    place = data["result"]
    return JsonResponse({
        "name": place.get("name"),
        "address": place.get("formatted_address"),
        "image": place.get("photos", [{}])[0].get("photo_reference", ""),
        "description": place.get("editorial_summary", {}).get("overview", "No description available"),
        "reviews": [review["text"] for review in place.get("reviews", [])]
    })