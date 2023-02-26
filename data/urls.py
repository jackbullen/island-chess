from django.urls import path
from . import views

# app_name = 'games'

urlpatterns = [
    path('games/', views.GameListView.as_view(), name='games'),
    path('openings', views.openings_list, name='openings'),
    path('openings/<int:pk>', views.opening_detail, name='opening_detail'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    # path('games/filtered/', views.games_list_filtered, name='games_list_filtered')

]