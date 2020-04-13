""" URL Configuration """
from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/data', views.main_chart_data, name='main_chart_data'),
    path('dashboard/data/<str:type>', views.main_chart_data, name='main_chart_data'),
]