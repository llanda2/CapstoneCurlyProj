from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.hair_type_quiz, name='hair_type_quiz'),  # Show the quiz form
    path('products/', views.product_list, name='product_list'),  # Show the product list after quiz submission
]
