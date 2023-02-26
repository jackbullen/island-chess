from django.urls import path
from . import views

# app_name = 'games'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>', views.course_detail, name='course_detail'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('delete/', views.course_delete, name='course_delete'),

    path('chapter/<int:pk>', views.chapter_detail, name='chapter_detail'),
    path('chapter/create/<int:pk>', views.ChapterCreateView.as_view(), name='chapter_create'),
    path('chapter/delete/<int:pk>', views.chapter_delete, name='chapter_delete'),

    path('variation/<int:pk>', views.variation_detail, name='variation_detail'),
    path('variation/create/<int:pk>/', views.VariationCreateView.as_view(), name='variation_create'),
    path('variation/delete/<int:pk>/', views.variation_delete, name='variation_delete'),

    path('practice/<int:pk>/', views.practice, name='practice'), 
    path('practice/variation/<int:pk>/', views.variation_practice, name='variation_practice'),
    path('practice/chapter/<int:pk>/', views.chapter_practice, name='chapter_practice'),

    path('learn/<int:pk>/', views.learn, name='learn'),
    path('learn/variation/<int:pk>/', views.variation_learn, name='variation_learn'),
    path('learn/chapter/<int:pk>/', views.chapter_learn, name='chapter_learn'),

    path('get_variation_pgn/<int:pk>/', views.get_variation_pgn, name='get_variation_pgn'),

]
