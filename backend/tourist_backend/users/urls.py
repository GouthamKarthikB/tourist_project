from django.urls import path
from .views import RegisterView, LoginView,get_tourist_places , VisitCreateView , VisitListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("tourist-places/", get_tourist_places, name="tourist-places"),
    path('visits/', VisitCreateView.as_view(), name='create-visit'),
    path('visits/<str:place_id>/', VisitListView.as_view(), name='list-visitors'),
]