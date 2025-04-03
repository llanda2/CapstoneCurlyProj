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

            # Step 1: Get base products matching hair type, curl pattern, vegan, and price
            # Use .get() method with a default to avoid KeyError
            price_range = quiz_data.get('price_range')
            if price_range == "$":
                base_products = HairProduct.objects.filter(price__lte=12.00)
            elif price_range == "$$":
                base_products = HairProduct.objects.filter(price__gt=12.00, price__lte=25.00)
            else:
                base_products = HairProduct.objects.filter(price__gt=25.00)

            # Get the values from the form data
            hair_type = quiz_data.get('hair_type', '')
            curl_pattern = quiz_data.get('curl_pattern', '')
            vegan = quiz_data.get('vegan', False)
            scalp_condition = quiz_data.get('scalp_condition', 'normal')  # Add this line

            # Convert string vegan value to boolean if needed
            if isinstance(vegan, str):
                vegan = vegan.lower() in ('yes', 'true', 'y', 't', '1')

            # Then use these variables in the filter
            base_products = base_products.filter(
                hair_type__icontains=hair_type,
                curl_pattern__icontains=curl_pattern,
                vegan=vegan
            )

            print(f"After Base Filters: {base_products.count()} products")

            # Copy of base products for categorization
            all_matching_products = base_products

            # Step 2: Apply Growth Areas Filter if specified (with fallback handling)
            growth_areas = quiz_data.get('growth_areas', [])
            if growth_areas:
                # Create a Q object for each growth area
                growth_q_objects = [Q(growth_areas__icontains=area) for area in growth_areas]

                # Combine Q objects with OR operator
                if growth_q_objects:
                    growth_query = growth_q_objects[0]
                    for q_obj in growth_q_objects[1:]:
                        growth_query |= q_obj

                    # Apply filter
                    growth_filtered = base_products.filter(growth_query)
                    print(f"After Growth Areas Filter: {growth_filtered.count()} products")

                    # If we have results, use them; otherwise, stick with base_products
                    if growth_filtered.exists():
                        base_products = growth_filtered

            # Step 3: Optional Styling Product Filtering
            styling_product = quiz_data.get('styling_product')
            if styling_product:
                styling_filtered = base_products.filter(category__icontains=styling_product)
                print(f"After Styling Product Filter: {styling_filtered.count()} products")

                # Only apply if we get results, otherwise keep the broader set
                if styling_filtered.exists():
                    styling_products = styling_filtered
                else:
                    styling_products = base_products
            else:
                styling_products = base_products

            # Remove Duplicates
            styling_products = styling_products.distinct()
            all_matching_products = all_matching_products.distinct()

            # Routine steps mapping
            # Routine steps mapping
            routine_steps = {
                "Low": ["Shampoo", "Conditioner", "Curl Cream"],
                "Medium": ["Shampoo", "Conditioner", "Curl Cream", "Gel/Mousse"],
                "High": ["Shampoo", "Conditioner", "Leave-In", "Curl Cream", "Gel", "Mousse"]
            }

            # Get maintenance level with default
            # Convert to title case to match dictionary keys
            maintenance_level = quiz_data.get('maintenance', 'medium').title()            # Categorization based on product types
            steps_needed = routine_steps.get(maintenance_level, routine_steps['Medium'])  # Fallback if invalid value
            categorized_products = {}

            # Add special recommendations based on scalp condition
            special_recommendations = {}

            # For dry scalp, recommend oils
            if scalp_condition and scalp_condition.lower() == 'dry':
                oil_products = HairProduct.objects.filter(
                    category__icontains="Oil",
                    vegan=vegan,  # Maintain vegan preference
                )

                # Apply price filter to oils
                if price_range == "$":
                    oil_products = oil_products.filter(price__lte=12.00)
                elif price_range == "$$":
                    oil_products = oil_products.filter(price__gt=12.00, price__lte=25.00)
                else:
                    oil_products = oil_products.filter(price__gt=25.00)

                if oil_products.exists():
                    special_recommendations["Scalp Oil"] = list(oil_products)
                    print(f"Found {oil_products.count()} oil products for dry scalp")

            # For oily or flaky scalp, recommend hair masks; otherwise, recommend oils
            elif scalp_condition and scalp_condition.lower() in ['oily', 'flaky']:
                recommended_category = "Hair Mask" if scalp_condition.lower() == "flaky" else "Oil"

                recommended_products = HairProduct.objects.filter(
                    category__icontains=recommended_category,
                    vegan=vegan,  # Maintain vegan preference
                )

                # Apply price filtering
                if price_range == "$":
                    recommended_products = recommended_products.filter(price__lte=12.00)
                elif price_range == "$$":
                    recommended_products = recommended_products.filter(price__gt=12.00, price__lte=25.00)
                else:
                    recommended_products = recommended_products.filter(price__gt=25.00)

                if recommended_products.exists():
                    special_recommendations[recommended_category] = list(recommended_products)
                    print(
                        f"Found {recommended_products.count()} {recommended_category} products for {scalp_condition} scalp")

            for step in steps_needed:
                # Special handling for Mousse/Gel
                # For the product categorization section, update this part:
                if step == "Gel/Mousse" or step == "Mousse/Gel":
                    mousse_products = all_matching_products.filter(category__icontains="Mousse")
                    gel_products = all_matching_products.filter(category__icontains="Gel")
                    categorized_products[step] = list(mousse_products) + list(gel_products)
                # For styling product specifically requested by the user
                elif styling_product and step.lower() == styling_product.lower():
                    matching_products = styling_products.filter(category__icontains=step)
                    categorized_products[step] = list(matching_products)
                else:
                    # For each step, find products that contain that product type
                    matching_products = all_matching_products.filter(category__icontains=step)
                    categorized_products[step] = list(matching_products)

                print(f"Found {len(categorized_products[step])} products for {step}")
            print(f"Scalp Condition: {scalp_condition}")

            print("Final Categorized Products:", {k: len(v) for k, v in categorized_products.items()})
            print("Special Recommendations:", {k: len(v) for k, v in special_recommendations.items()})

            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
                'routine_steps': steps_needed,
                'special_recommendations': special_recommendations,  # Add this to the context
                'scalp_condition': scalp_condition,  # Pass this to the template
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
