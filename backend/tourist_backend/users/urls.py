from django.urls import path
from .views import RegisterView, LoginView,get_nearby_tourist_places

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("tourist-places/", get_nearby_tourist_places, name="tourist-places"),
]
