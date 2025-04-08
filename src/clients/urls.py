from django.urls import path
from . import views

urlpatterns = [
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    ]