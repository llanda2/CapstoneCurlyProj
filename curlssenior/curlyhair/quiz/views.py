from django.shortcuts import render
from .forms import HairTypeForm
from .models import HairProduct  # Import the model to filter products


def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairTypeForm(request.POST)
        if form.is_valid():
            selected_types = form.cleaned_data['curl_pattern']
            # Filter the products based on selected curl patterns
            products = HairProduct.objects.filter(curl_pattern__in=selected_types)
            return render(request, 'quiz/product_list.html', {'products': products})
    else:
        form = HairTypeForm()

    return render(request, 'quiz/hair_type_quiz.html', {'form': form})


# Add this view to render the product list after the quiz is completed
def product_list(request):
    # You might need to pass the selected product list (either through context or session)
    products = HairProduct.objects.all()  # Or filter based on quiz results
    return render(request, 'quiz/product_list.html', {'products': products})
