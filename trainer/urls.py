from django.urls import path
from . import views

urlpatterns = [
    path('', views.repertoire_list, name='repertoire_list'),
    path('repertoire/<int:pk>/', views.repertoire_detail, name='repertoire_detail'),
    path('repertoire/create/', views.RepertoireCreateView.as_view(), name='create_repertoire'),
    path('opening/<int:pk>/', views.opening_detail, name='opening_detail'),
    path('opening/create/<int:pk>/', views.OpeningCreateView.as_view(), name='create_opening'),
    path('opening/delete/<int:pk>/', views.opening_delete, name='opening_delete'),
    path('line/<int:pk>/', views.line_detail, name='line_detail'),
    path('line/create/<int:pk>/', views.LineCreateView.as_view(), name='create_line'),
    path('variation/<int:pk>/', views.variation_detail, name='variation_detail'),
    path('variation/create/<int:pk>/', views.VariationCreateView.as_view(), name='create_variation'),
    path('practice/<int:pk>', views.practice, name='practice'),

]
