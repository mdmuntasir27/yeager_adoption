from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:pet_pk>/', views.apply_adoption, name='apply_adoption'),
    path('my-requests/', views.my_requests, name='my_requests'),
]

