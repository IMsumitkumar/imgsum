from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('img/<str:token>/', views.shortner_target, name='shortner_target'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add_photo'),
    path('like/', views.like_photo, name='like-post'),

    path('post-comment/',views.post_comment, name='post-comment'),
]