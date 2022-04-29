from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),

]