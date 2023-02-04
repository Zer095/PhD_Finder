from django.urls import path
from . import views

app_name = 'positions'

urlpatterns = [
    # ex: /positions/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /ìpositions/Europe/
    path('view/<str:region>/', views.RegionView.as_view(), name='detail'),
    # ex: /positions/5/
    path('<int:pk>/', views.DescriptionView.as_view(), name='description'),
    # ex: /positions/register/
    path('register/', views.register_request, name='register'),
    # ex: /positions/login/
    path('login/', views.login_request, name='login'),
    # ex: /positions/logout/
    path('logout/', views.logout_request, name='logout'),
    # ex: /positions/all_position
    path('all_position/', views.LastPositionView.as_view(), name='all_pos'), 
    # ex: /positions/about
    path('about/', views.AboutView, name='about'),                                              
]