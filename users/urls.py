from django.urls import path
from . import views


urlpatterns = [
    # path('profile/', views.user_profile, name='user-profile'),

    path('<str:pk>/profile/', views.user_profile, name='user-profile')
]