# views.py
from django.shortcuts import render
from .models import HairProduct, HairQuiz  # Make sure HairQuiz is imported
from .forms import HairQuizForm


# Home view
def home(request):
    return render(request, 'quiz/home.html')  # You can render a template here


def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            hair_type = form.cleaned_data['hair_type']
            vegan = form.cleaned_data['vegan']
            maintenance_level = form.cleaned_data['maintenance_level']

            # Debugging: Print quiz results
            print(f"Quiz Results: Hair Type: {hair_type}, Vegan: {vegan}, Maintenance Level: {maintenance_level}")

            # Get all products and print for debugging
            all_products = HairProduct.objects.all()
            print(f"Total Products in DB: {all_products.count()}")

            for product in all_products:
                print(f"{product.name} | Hair Type: {product.hair_type} | Vegan: {product.vegan} | Category: {product.category}")

            # Convert vegan to a boolean if needed
            if isinstance(vegan, str):
                vegan = vegan.lower() == 'true'

            # Filtering logic with contains for hair type
            products = HairProduct.objects.filter(
                hair_type__icontains=hair_type,
                vegan=vegan
            )

            # Debugging: Print filtered products
            print(f"Filtered Products Count: {products.count()}")
            for product in products:
                print(f"Filtered Product: {product.name}")

            # Define categories
            categories = ['Shampoo', 'Conditioner', 'Leave-in', 'Curl Cream', 'Gel', 'Mousse']
            categorized_products = {category: [] for category in categories}

            # Group products by category
            for product in products:
                if product.category in categories:
                    categorized_products[product.category].append(product)

            # Maintenance Level determines the routine steps:
            routine_steps = {
                "Low": 3,    # 3-step routine (Shampoo, Conditioner, Leave-in)
                "Medium": 4, # 4-step routine (Shampoo, Conditioner, Leave-in, Curl Cream)
                "High": 5    # 5-step routine (Shampoo, Conditioner, Leave-in, Curl Cream, Gel)
            }

            # Select only the number of products needed for the routine
            selected_products = {}
            step_count = routine_steps.get(maintenance_level, 3)

            # Ensure we only return the necessary steps
            required_categories = categories[:step_count]  # Get only the needed categories
            for category in required_categories:
                if categorized_products[category]:  # Ensure there's at least one product
                    selected_products[category] = categorized_products[category][0]  # Pick the first matching product

            return render(request, 'quiz/results.html', {
                'selected_products': selected_products,
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
