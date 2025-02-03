# views.py
from django.shortcuts import render
from .models import HairProduct, HairQuiz  # Make sure HairQuiz is imported
from .forms import HairQuizForm


# Home view
def home(request):
    return render(request, 'quiz/home.html')  # You can render a template here


# Hair type quiz view
def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            # Process the form data
            hair_type = form.cleaned_data['hair_type']
            curl_pattern = form.cleaned_data['curl_pattern']
            vegan = form.cleaned_data['vegan']
            weight = form.cleaned_data['weight']

            # You can process or store this data here
            # For now, we will render the results page
            return render(request, 'quiz/results.html', {
                'hair_type': hair_type,
                'curl_pattern': curl_pattern,
                'vegan': vegan,
                'weight': weight
            })
    else:
        form = HairQuizForm()

    return render(request, 'quiz/hair_type_quiz.html', {'form': form})


def quiz(request):
    if request.method == 'POST':
        curl_pattern = request.POST.get('curl_pattern')
        hair_type = request.POST.get('hair_type')
        vegan = 'vegan' in request.POST

        # Save quiz responses to the database (optional)
        HairQuiz.objects.create(curl_pattern=curl_pattern, hair_type=hair_type, vegan_preference=vegan)

        # Filter products based on quiz answers
        recommended_products = HairProduct.objects.filter(
            curl_pattern__contains=curl_pattern,
            hair_type__contains=hair_type,
            vegan=vegan
        )

        return render(request, 'quiz/results.html', {'products': recommended_products})

    return render(request, 'quiz/quiz.html')
