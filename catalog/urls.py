from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('collection/', views.collection_list, name='collection_list'),
    path('collection/my/', views.my_collection, name='my_collection'),
    path('collection/all/', views.all_collection, name='all_collection'),
    path('milk-jug/<int:pk>/', views.milk_jug_detail, name='milk_jug_detail'),
    path('milk-jug/create/', views.milk_jug_create, name='milk_jug_create'),
    path('milk-jug/<int:pk>/update/', views.milk_jug_update, name='milk_jug_update'),
    path('milk-jug/<int:pk>/delete/', views.milk_jug_delete, name='milk_jug_delete'),
    path('milk-jug/<int:pk>/photo/upload/', views.photo_upload, name='photo_upload'),
    path('milk-jug/<int:pk>/photo/<int:photo_id>/delete/', views.photo_delete, name='photo_delete'),
    path('milk-jug/<int:pk>/photo/<int:photo_id>/set-main/', views.photo_set_main, name='photo_set_main'),
]
