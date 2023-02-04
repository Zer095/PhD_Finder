from django.urls import path

from .import views

app_name = 'users'

urlpatterns = [
    # Profile 
    path('profile/', views.profile, name='users-profile'),
    # Saved Positions
    path('saved/', views.SavedView.as_view(), name='saved'),
    # Second profile
    path('prof1/', views.EditProfile, name='profile'),
] 