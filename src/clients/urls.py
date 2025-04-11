from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('notifications/', views.notification_dashboard, name='notification_dashboard'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/read/', views.read_notifications, name='read_notifications'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('add-client/', views.add_client, name='add_client'),
    path('client/<int:client_id>/edit/', views.edit_client, name='edit_client'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)