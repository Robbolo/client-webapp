from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('notifications/', views.notification_dashboard, name='notification_dashboard'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/read/', views.read_notifications, name='read_notifications'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail')
    ]