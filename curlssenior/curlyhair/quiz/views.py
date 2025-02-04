# views.py
from django.shortcuts import render
from .models import HairProduct, HairQuiz  # Make sure HairQuiz is imported
from .forms import HairQuizForm


# Home view
def home(request):
    return render(request, 'quiz/home.html')  # You can render a template here


from django.shortcuts import render
from .forms import HairQuizForm

def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            # Retrieve the cleaned data from the form
            hair_type = form.cleaned_data['hair_type']  # "Thin", "Medium", "Thick"
            curl_pattern = form.cleaned_data['curl_pattern']  # "2A", "3B", etc.
            vegan = form.cleaned_data['vegan']  # True or False
            maintenance_level = form.cleaned_data['maintenance_level'].lower()  # "low", "medium", "high"

            # Debugging: Print quiz results to ensure correct data is captured
            print(f"Quiz Results: Hair Type: {hair_type}, Curl Pattern: {curl_pattern}, Vegan: {vegan}, Maintenance Level: {maintenance_level}")

            # Define product types for each maintenance level
            maintenance_mapping = {
                "low": ["Shampoo", "Conditioner", "Curl Cream"],
                "medium": ["Shampoo", "Conditioner", "Leave-In", "Mousse/Foam"],
                "high": ["Shampoo", "Conditioner", "Curl Cream", "Leave-In", "Gel", "Mousse/Foam"]
            }

            # Get allowed product types for the selected maintenance level
            allowed_product_types = maintenance_mapping.get(maintenance_level, [])

            # Filter products based on quiz results
            products = HairProduct.objects.filter(
                hair_type__icontains=hair_type,  # Match hair type
                curl_pattern__icontains=curl_pattern,  # Match curl pattern
                vegan=vegan,  # Match vegan preference
                category__in=allowed_product_types  # Match maintenance-level product types
            )

            # Debugging: Print filtered products count
            print(f"Filtered Products Count: {products.count()}")
            for product in products:
                print(f"Filtered Product: {product.name} - {product.category} (Hair Type: {product.hair_type}, Curl Pattern: {product.curl_pattern}, Vegan: {product.vegan})")

            # Organizing products by category (Shampoo, Conditioner, etc.)
            categorized_products = {category: [] for category in allowed_product_types}

            for product in products:
                if product.category in allowed_product_types:
                    categorized_products[product.category].append(product)

            # Render the results template with categorized products
            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
                'maintenance_level': maintenance_level
            })

    else:
        # If the form is not submitted yet, initialize the empty form
        form = HairQuizForm()

    # Render the quiz page with the form
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
