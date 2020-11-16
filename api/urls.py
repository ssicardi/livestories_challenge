from django.urls import path

from . import views

urlpatterns = [
    path('unique/', views.getUniqueEvents, name='getUniqueEvents'),
    path('histogram/<str:event>/<str:date>/', views.histogramFromDate, name='histogramFromDate'),
    path('<str:event>/', views.countEvent, name='countEvent'),
    path('<str:event>/<int:count>/', views.countEvent, name='countEvent'),
    path('', views.getEventsFromDates, name='getEventsFromDates'),
]
