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


def helpful_tips(request):
    return render(request, 'quiz/helpful_tips.html')


import re
from django.shortcuts import render
from django.db.models import Q


def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            quiz_data = form.cleaned_data
            print("📋 Quiz Data:", quiz_data)

            # Get user selections
            price_range = quiz_data.get('budget')  # updated from 'price_range'
            print("💸 Budget selected from form:", price_range)

            hair_type = quiz_data.get('hair_type', '')
            curl_pattern = quiz_data.get('curl_pattern', '')
            vegan = quiz_data.get('vegan', False)
            scalp_condition = quiz_data.get('scalp_condition', 'normal')
            styling_product = quiz_data.get('styling_product')

            if isinstance(vegan, str):
                vegan = vegan.lower() in ('yes', 'true', 'y', 't', '1')

            # Filter by price range
            if price_range == "$":
                base_products = HairProduct.objects.filter(price__lte=12.00)
            elif price_range == "$$":
                base_products = HairProduct.objects.filter(price__gt=12.00, price__lte=25.00)
            else:
                base_products = HairProduct.objects.filter(price__gt=25.00)

            print("🧼 Products after price filter:")
            for p in base_products:
                print(f"- {p.brand} {p.name} | ${p.price}")

            # Filter further by curl, hair type, vegan
            base_products = base_products.filter(
                hair_type__icontains=hair_type,
                curl_pattern__icontains=curl_pattern,
                vegan=vegan
            )

            print(f"✅ Products after all filters: {base_products.count()} found")

            all_matching_products = base_products.distinct()

            # Apply Growth Areas Filter
            growth_areas = quiz_data.get('growth_areas', [])
            if growth_areas:
                growth_q_objects = [Q(growth_areas__icontains=area) for area in growth_areas]
                growth_query = growth_q_objects[0]
                for q in growth_q_objects[1:]:
                    growth_query |= q
                growth_filtered = base_products.filter(growth_query)
                print(f"🌱 After Growth Area filter: {growth_filtered.count()} found")
                if growth_filtered.exists():
                    base_products = growth_filtered
                    all_matching_products = base_products.distinct()

            # Styling product filter (optional)
            if styling_product:
                styling_filtered = base_products.filter(category__icontains=styling_product)
                print(f"🎨 After Styling Product filter: {styling_filtered.count()} found")
                styling_products = styling_filtered if styling_filtered.exists() else base_products
            else:
                styling_products = base_products

            styling_products = styling_products.distinct()

            # Routine Steps
            routine_steps = {
                "Low": ["Shampoo", "Conditioner", "Curl Cream"],
                "Medium": ["Shampoo", "Conditioner", "Curl Cream", "Gel/Mousse"],
                "High": ["Shampoo", "Conditioner", "Leave-In", "Curl Cream", "Gel", "Mousse"]
            }

            maintenance_level = quiz_data.get('maintenance', 'medium').title()
            steps_needed = routine_steps.get(maintenance_level, routine_steps['Medium'])

            categorized_products = {}

            for step in steps_needed:
                if step in ["Gel/Mousse", "Mousse/Gel"]:
                    mousse_products = all_matching_products.filter(category__icontains="Mousse")
                    gel_products = all_matching_products.filter(category__icontains="Gel")
                    combined = list(mousse_products) + list(gel_products)
                    deduped = {
                        f"{p.name.strip().lower()}__{p.brand.strip().lower()}": p
                        for p in combined
                    }.values()
                    categorized_products[step] = list(deduped)

                elif styling_product and step.lower() == styling_product.lower():
                    matching_products = styling_products.filter(category__icontains=step)
                    deduped = {
                        f"{p.name.strip().lower()}__{p.brand.strip().lower()}": p
                        for p in matching_products
                    }.values()
                    categorized_products[step] = list(deduped)

                else:
                    matching_products = all_matching_products.filter(category__icontains=step)
                    deduped = {
                        f"{p.name.strip().lower()}__{p.brand.strip().lower()}": p
                        for p in matching_products
                    }.values()
                    categorized_products[step] = list(deduped)

                print(f"🧴 {step}: {len(categorized_products[step])} unique products")

            # Scalp Condition — optional section (simplified for now)
            special_recommendations = {}  # Add your scalp logic here later if needed

            return render(request, 'quiz/results.html', {
                'categorized_products': categorized_products,
                'routine_steps': steps_needed,
                'special_recommendations': special_recommendations,
                'scalp_condition': scalp_condition,
            })

    else:
        form = HairQuizForm()

    curl_type_image_map = {
        "2A": "TwoA.png", "2B": "TwoB.png", "2C": "TwoC.png",
        "3A": "ThreeA.png", "3B": "ThreeB.png", "3C": "ThreeC.png",
        "4A": "FourA.png", "4B": "FourB.png", "4C": "FourC.png",
    }

    return render(request, 'quiz/hair_type_quiz.html', {
        'form': form,
        'curl_type_image_map': curl_type_image_map,
    })


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


# Add to your views.py file

from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context, Template
from xhtml2pdf import pisa
from io import BytesIO
from django.utils.text import slugify
from datetime import datetime
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


def save_routine_pdf(request):
    """Generate and return a PDF of the user's curl routine"""
    if request.method == 'POST':
        try:
            routine_data_raw = request.POST.get('routine_data', '{}')
            print("RAW routine data string:", routine_data_raw)

            try:
                routine_data = json.loads(routine_data_raw)
                print("Parsed routine data:", json.dumps(routine_data, indent=2))  # 👈 formatted debug output
            except json.JSONDecodeError:
                logger.error("Invalid JSON data received")
                return HttpResponse("Invalid data format. Please try again.", status=400)

            # Log data for debugging
            logger.debug(f"Received routine data: {routine_data}")

            # Create a context with the data
            context = {
                'routine_data': routine_data,
                'generated_date': datetime.now().strftime('%B %d, %Y'),
            }

            # Get template and render it with context
            template = get_template('quiz/routine_pdf_template.html')
            html = template.render(context)

            # Create PDF response
            buffer = BytesIO()

            # Create PDF
            pdf_status = pisa.CreatePDF(
                html,
                dest=buffer,
                encoding='UTF-8'
            )

            if not pdf_status.err:
                # Success - return PDF file for download
                buffer.seek(0)
                filename = f"curl_routine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                # Log the error
                logger.error(f"PDF generation error: {pdf_status.err}")
                return HttpResponse("Error generating PDF. Please try again.", status=500)

        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return HttpResponse("Invalid data format. Please try again.", status=400)
        except Exception as e:
            logger.exception("Error in PDF generation")
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("This endpoint requires a POST request with routine data.", status=400)
    return render(request, 'quiz/your_results_template.html', context)