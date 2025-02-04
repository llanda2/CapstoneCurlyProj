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
            hair_type = form.cleaned_data['hair_type']  # e.g., "Thin"
            curl_pattern = form.cleaned_data['curl_pattern']  # e.g., "2A"
            vegan = form.cleaned_data['vegan']  # This will be either True or False
            maintenance_level = form.cleaned_data['maintenance_level']  # e.g., "Low"

            # Debugging: Print the quiz results to ensure we're capturing data correctly
            print(f"Quiz Results: Hair Type: {hair_type}, Curl Pattern: {curl_pattern}, Vegan: {vegan}, Maintenance Level: {maintenance_level}")

            # Get all products in the database
            all_products = HairProduct.objects.all()
            print(f"Total Products in DB: {all_products.count()}")

            # Filtering the products based on quiz results
            products = HairProduct.objects.filter(
                hair_type__icontains=hair_type,  # Match hair type (using 'icontains' for case-insensitive)
                curl_pattern__icontains=curl_pattern,  # Match curl pattern (using 'icontains' for case-insensitive)
                vegan=vegan  # Only return products that match the vegan preference (True or False)
            )

            # Debugging: Print the filtered products count and their details
            print(f"Filtered Products Count: {products.count()}")
            for product in products:
                print(f"Filtered Product: {product.name} - Hair Type: {product.hair_type}, Curl Pattern: {product.curl_pattern}, Vegan: {product.vegan}")

            # Organizing products by category (e.g., Shampoo, Conditioner, etc.)
            categories = ['Shampoo', 'Conditioner', 'Leave-in', 'Curl Cream', 'Gel', 'Mousse']
            categorized_products = {category: [] for category in categories}

            # Sort the products into their respective categories
            for product in products:
                if product.category in categories:
                    categorized_products[product.category].append(product)

            # Render the results template with categorized products
            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
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
