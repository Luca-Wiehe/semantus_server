from django.urls import path
from . import views

urlpatterns = [
   path('', views.HomepageView.as_view(), name='homepage-view'),
   path('signup/', views.SignupView.as_view(), name='signup'),
   path('login/', views.LoginView.as_view(), name='login'),
]