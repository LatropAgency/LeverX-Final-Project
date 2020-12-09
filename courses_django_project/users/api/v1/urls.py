from django.urls import path
from users.api.v1 import views

urlpatterns = [
    path('users/', views.UserView.as_view()),
]