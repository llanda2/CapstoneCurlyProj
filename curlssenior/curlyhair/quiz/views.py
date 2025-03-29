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
from django.shortcuts import render
from django.db.models import Q


def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            quiz_data = form.cleaned_data
            print("Quiz Data:", quiz_data)

            # Step 1: Price Filtering
            if quiz_data['price_range'] == "$":
                products = HairProduct.objects.filter(price__lte=12.00)
            elif quiz_data['price_range'] == "$$":
                products = HairProduct.objects.filter(price__gt=12.00, price__lte=25.00)
            else:
                products = HairProduct.objects.filter(price__gt=25.00)

            print(f"After Price Filter: {products.count()} products")

            # Step 2: Hair Type & Vegan Filtering
            products = products.filter(
                hair_type__icontains=quiz_data['hair_type'],
                curl_pattern__icontains=quiz_data['curl_pattern'],
                vegan=quiz_data['vegan']
            )

            print(f"After Hair Type & Vegan Filter: {products.count()} products")

            # Step 3: Styling Product Filtering - Only if user selected one
            # This should probably be optional, as it's restricting results too much
            if quiz_data.get('styling_product'):
                styling_filtered = products.filter(category__icontains=quiz_data['styling_product'])
                print(f"After Styling Product Filter: {styling_filtered.count()} products")

                # Only apply if we get results, otherwise keep the broader set
                if styling_filtered.exists():
                    products = styling_filtered

            # Step 4: Growth Areas Filtering (With Fallback)
            if quiz_data.get('growth_areas') and quiz_data['growth_areas']:
                growth_area_filtered = products.filter(
                    Q(*[Q(growth_areas__icontains=area) for area in quiz_data['growth_areas']], _connector=Q.OR)
                )
                if growth_area_filtered.exists():
                    products = growth_area_filtered

            print(f"After Growth Areas Filter: {products.count()} products")

            # Remove Duplicates
            products = products.distinct()

            # Routine steps mapping
            routine_steps = {
                "Low": ["Shampoo", "Conditioner", "Curl Cream"],
                "Medium": ["Shampoo", "Conditioner", "Leave-In", "Mousse/Gel"],
                "High": ["Shampoo", "Conditioner", "Curl Cream", "Leave-In", "Gel", "Mousse"]
            }

            # Get all products for initial categorization before filtering by styling_product
            all_matching_products = HairProduct.objects.filter(
                hair_type__icontains=quiz_data['hair_type'],
                curl_pattern__icontains=quiz_data['curl_pattern'],
                vegan=quiz_data['vegan']
            )

            if quiz_data['price_range'] == "$":
                all_matching_products = all_matching_products.filter(price__lte=12.00)
            elif quiz_data['price_range'] == "$$":
                all_matching_products = all_matching_products.filter(price__gt=12.00, price__lte=25.00)
            else:
                all_matching_products = all_matching_products.filter(price__gt=25.00)

            # Apply growth areas filter if specified
            if quiz_data.get('growth_areas') and quiz_data['growth_areas']:
                growth_area_filtered = all_matching_products.filter(
                    Q(*[Q(growth_areas__icontains=area) for area in quiz_data['growth_areas']], _connector=Q.OR)
                )
                if growth_area_filtered.exists():
                    all_matching_products = growth_area_filtered

            # Categorization based on product types
            steps_needed = routine_steps[quiz_data['maintenance_level']]
            categorized_products = {}

            for step in steps_needed:
                # Replace Mousse/Gel with two separate searches if needed
                if step == "Mousse/Gel":
                    mousse_products = all_matching_products.filter(category__icontains="Mousse")
                    gel_products = all_matching_products.filter(category__icontains="Gel")
                    categorized_products["Mousse/Gel"] = list(mousse_products) + list(gel_products)
                else:
                    # For each step, find products that contain that product type
                    matching_products = all_matching_products.filter(category__icontains=step)
                    categorized_products[step] = list(matching_products)

                print(f"Found {len(categorized_products[step])} products for {step}")

            # If user specifically wanted a styling product, ensure it's included
            if quiz_data.get('styling_product'):
                styling_step = quiz_data['styling_product']
                if styling_step in steps_needed:
                    # Override with filtered products if we have any
                    styling_products = products.filter(category__icontains=styling_step)
                    if styling_products.exists():
                        categorized_products[styling_step] = list(styling_products)

            print("Final Categorized Products:", {k: len(v) for k, v in categorized_products.items()})

            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
                'routine_steps': steps_needed,
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
