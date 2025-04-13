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
    path('client/<int:client_id>/add-session/', views.add_session, name='add_session'),
    path('session/<int:session_id>/complete/', views.mark_session_completed, name='mark_session_completed'),
    path('session/<int:session_id>/no-show/', views.mark_session_no_show, name='mark_session_no_show'),
    path('session/<int:session_id>/undo/', views.undo_session_status, name='undo_session_status'),
    path('sessions/upcoming/', views.upcoming_sessions, name='upcoming_sessions'),
    path('client/<int:client_id>/upload-document/', views.upload_document, name='upload_document'),
    path('document/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)