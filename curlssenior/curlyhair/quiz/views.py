from .forms import HairQuizForm
from .models import HairProduct, HairQuiz
from django.shortcuts import render, redirect
from quiz.models import TriedProduct  # Import the model
from .forms import TriedProductForm


def home(request):
    # Debug: Print the logged products to check if they're fetched
    logged_products = TriedProduct.objects.all()
    print("Logged Products for Home Page:", logged_products)  # Debugging line

    return render(request, 'home.html', {
        'logged_products': logged_products
    })


import re


def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            quiz_data = form.cleaned_data

            print("\n=== Quiz Data ===")
            print(quiz_data)

            # Step 1: Price Filtering
            if quiz_data['price_range'] == "$":
                products = HairProduct.objects.filter(price__lte=12.00)
            elif quiz_data['price_range'] == "$$":
                products = HairProduct.objects.filter(price__gt=12.00, price__lte=25.00)
            else:
                products = HairProduct.objects.filter(price__gt=25.00)

            print("\n=== After Price Filter ===")
            for product in products:
                print(f"{product.name} - {product.category}")

            # Step 2: Hair Type & Vegan Filtering
            products = products.filter(
                hair_type__icontains=quiz_data['hair_type'],
                curl_pattern__icontains=quiz_data['curl_pattern'],
                vegan=quiz_data['vegan']
            )

            print("\n=== After Hair Type & Vegan Filter ===")
            if not products.exists():
                print("No products left after Hair Type & Vegan filter!")
            for product in products:
                print(f"{product.name} - {product.category}")

            # Step 3: Styling Product Filtering
            products = products.filter(category__icontains=quiz_data['styling_product'])

            print("\n=== After Styling Product Filter ===")
            if not products.exists():
                print("No products left after Styling Product filter!")
            for product in products:
                print(f"{product.name} - {product.category}")

            # Step 4: Growth Areas Filtering with Fallback
            if quiz_data.get('growth_areas'):
                growth_area_filtered = products.filter(
                    growth_areas__iregex=r'|'.join(quiz_data['growth_areas'])
                )

                if growth_area_filtered.exists():
                    products = growth_area_filtered

            print("\n=== After Growth Areas Filter ===")
            if not products.exists():
                print("No products left after Growth Areas filter!")
            for product in products:
                print(f"{product.name} - {product.category}")

            # Routine steps
            routine_steps = {
                "Low": ["Shampoo", "Conditioner", "Curl Cream"],
                "Medium": ["Shampoo", "Conditioner", "Leave-In", "Mousse/Gel"],
                "High": ["Shampoo", "Conditioner", "Curl Cream", "Leave-In", "Gel", "Mousse"]
            }

            # Categorizing products with more flexible matching
            categorized_products = {step: [] for step in routine_steps[quiz_data['maintenance_level']]}

            print("\n=== Final Queryset Before Categorization ===")
            for product in products:
                category = getattr(product, 'category', 'MISSING')
                print(f"{product.name} - {category}")
                if category == 'MISSING':
                    print("WARNING: Missing category for product!")

            for product in products:
                for step in categorized_products:
                    step_pattern = rf'\b{re.escape(step)}\b'  # Ensures word-boundary matching
                    if re.search(step_pattern, product.category, re.IGNORECASE):
                        categorized_products[step].append(product)

            print("\n=== Final Categorized Products ===")
            print(categorized_products)

            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
                'routine_steps': routine_steps[quiz_data['maintenance_level']],
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
