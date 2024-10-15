
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
      path('video_call/<str:meeting_code>/', views.video_call_view, name='video_call'), 
        path('join/<str:meeting_code>/', views.join_meeting_view, name='join_meeting'),
    # other URLs
]
