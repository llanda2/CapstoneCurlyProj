from django.shortcuts import render

def home(request):
    return render(request, 'quiz/home.html')  # ✅ Ensure correct template path

def hair_type_quiz(request):
    return render(request, 'quiz/hair_type_quiz.html')  # ✅ This must match the actual template path
