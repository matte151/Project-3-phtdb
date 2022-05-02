from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('pets/', views.pets_index, name='index'),
  path('pets/<int:pet_id>/', views.pets_detail, name='detail'),
  path('pets/create/', views.PetCreate.as_view(), name='pets_create'),
  path('pets/<int:pk>/update/', views.PetUpdate.as_view(), name='pets_update'),
  path('pets/<int:pk>/delete/', views.PetDelete.as_view(), name='pets_delete'),
  path('pets/<int:pet_id>/add_photo/', views.add_photo, name='add_photo'),
  # path('pets/<int:pet_id>/add_checkup/', views.add_checkup, name='add_checkup'),
  # path('pets/<int:pet_id>/add_profile/', views.add_profile, name='add_profile'),
  # path('pets/<int:pet_id>/add_note/', views.add_note, name='add_note'),
  # path('pets/<int:pet_id>/add_people/', views.add_people, name='add_people'),

  
  path('accounts/signup/', views.signup, name='signup'),

]