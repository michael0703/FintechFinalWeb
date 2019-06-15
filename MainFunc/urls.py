from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage, name='MainPage'),
    path('ListDB', views.ListDB, name='ListDB'),
    path('Analyze', views.Analyze, name='Analyze'),
    path('Query', views.Query, name='Query'),
    path('QueryNonuniform', views.QueryNonuniform, name='QueryNonuniform'),
    path('Process/', views.Process, name='Process'),

]
