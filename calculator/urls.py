from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_distance, name='index'),
    path('history/', views.history, name='history'),
    path('api/autocomplete/', views.autocomplete_api, name='autocomplete_api'),

]
