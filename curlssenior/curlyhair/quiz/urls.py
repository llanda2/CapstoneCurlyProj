from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ✅ Home page
    path('quiz/', views.hair_type_quiz, name='hair_type_quiz'),  # ✅ Quiz page
    path('tried-that/', views,tried_that_view, name='tried_that'),
]
