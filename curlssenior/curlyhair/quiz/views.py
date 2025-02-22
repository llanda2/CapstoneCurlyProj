from django.shortcuts import render, redirect
from .models import HairProduct, HairQuiz, TriedProduct
from .forms import HairQuizForm, TriedProductForm
from django.shortcuts import render
from .models import TriedProduct


# Home view
def home(request):
    logged_products = TriedProduct.objects.all()  # Fetch all logged products
    return render(request, 'home.html', {'logged_products': logged_products})


# Hair type quiz view
def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            hair_type = form.cleaned_data['hair_type']
            curl_pattern = form.cleaned_data['curl_pattern']
            vegan = form.cleaned_data['vegan']
            maintenance_level = form.cleaned_data['maintenance_level']
            price_range = form.cleaned_data['price_range']

            print(
                f"Quiz Results: Hair Type: {hair_type}, Curl Pattern: {curl_pattern}, Vegan: {vegan}, Maintenance Level: {maintenance_level}, Price: {price_range}")

            # Price filtering
            if price_range == "$":
                products = HairProduct.objects.filter(price__lte=12.00)
            elif price_range == "$$":
                products = HairProduct.objects.filter(price__gt=12.00, price__lte=25.00)
            else:  # "$$$"
                products = HairProduct.objects.filter(price__gt=25.00)

            # Further filter based on user input
            products = products.filter(
                hair_type__icontains=hair_type,
                curl_pattern__icontains=curl_pattern,
                vegan=vegan
            )

            # Routine structure based on maintenance level
            routine_steps = {
                "Low": ["Shampoo", "Conditioner", "Curl Cream"],
                "Medium": ["Shampoo", "Conditioner", "Leave-In", "Mousse/Foam"],
                "High": ["Shampoo", "Conditioner", "Curl Cream", "Leave-In", "Gel", "Mousse/Foam"]
            }

            # Categorize products into routine steps
            categorized_products = {step: [] for step in routine_steps[maintenance_level]}
            for product in products:
                if product.category in categorized_products:
                    categorized_products[product.category].append(product)

            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
                'routine_steps': routine_steps[maintenance_level],
            })
    else:
        form = HairQuizForm()

    return render(request, 'quiz/hair_type_quiz.html', {'form': form})


# Quiz view
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


from django.shortcuts import render, redirect
from .models import TriedProduct
from .forms import TriedProductForm


def tried_that(request):
    if request.method == "POST":
        form = TriedProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tried_that')  # Redirect back to the same page
    else:
        form = TriedProductForm()

    # Fetch all logged products
    logged_products = TriedProduct.objects.all()
    return render(request, 'quiz/tried_that.html', {
        'form': form,
        'logged_products': logged_products
    })
