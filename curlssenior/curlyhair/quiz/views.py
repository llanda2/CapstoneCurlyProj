from .forms import HairQuizForm
from .models import HairProduct, HairQuiz
from django.shortcuts import render, redirect
from quiz.models import TriedProduct  # Import the model
from .forms import TriedProductForm


def home(request):
    # Debug: Print the logged products to check if they're fetched
    logged_products = TriedProduct.objects.all()

    return render(request, 'home.html', {
        'logged_products': logged_products
    })


def helpful_tips(request):
    return render(request, 'quiz/helpful_tips.html')


import re
from django.shortcuts import render
from django.db.models import Q


from django.db.models import Q
from django.shortcuts import render
from .forms import HairQuizForm
from .models import HairProduct

def hair_type_quiz(request):
    if request.method == 'POST':
        form = HairQuizForm(request.POST)
        if form.is_valid():
            quiz_data = form.cleaned_data

            price_range = quiz_data.get('budget')
            hair_type = quiz_data.get('hair_type', '')
            curl_pattern = quiz_data.get('curl_type', '')
            vegan = quiz_data.get('vegan', 'no') == 'yes'
            hold_level = quiz_data.get('hold', '')
            scalp_condition = quiz_data.get('scalp_condition', '')
            color_treated = quiz_data.get('color_treated', 'no') == 'yes'
            maintenance_level = quiz_data.get('maintenance', 'medium').title()

            if price_range == "$":
                base_products = HairProduct.objects.filter(price__lte=12.00)
            elif price_range == "$$":
                base_products = HairProduct.objects.filter(price__gt=12.00, price__lte=25.00)
            else:
                base_products = HairProduct.objects.filter(price__gt=25.00)

            if color_treated:
                base_products = base_products.filter(sulfate_free__iexact='Yes')

            base_products = base_products.filter(
                hair_type__icontains=hair_type,
                curl_pattern__icontains=curl_pattern,
                vegan=vegan
            )

            all_matching_products = base_products.distinct()

            routine_steps = {
                "Low": ["Shampoo", "Conditioner", "Curl Cream"],
                "Medium": ["Shampoo", "Conditioner", "Curl Cream", "Gel/Mousse"],
                "High": ["Shampoo", "Conditioner", "Leave-In", "Curl Cream", "Gel", "Mousse"]
            }

            steps_needed = routine_steps.get(maintenance_level, routine_steps["Medium"])
            categorized_products = {}

            for step in steps_needed:
                if step in ["Gel/Mousse", "Mousse/Gel"]:
                    mousse = all_matching_products.filter(category__icontains="Mousse")
                    gel = all_matching_products.filter(category__icontains="Gel")
                    combined = list(mousse) + list(gel)
                else:
                    combined = all_matching_products.filter(category__icontains=step)

                deduped = {
                    f"{p.name.strip().lower()}__{p.brand.strip().lower()}": p
                    for p in combined
                }.values()
                categorized_products[step] = list(deduped)

            special_recommendations = {}

            def scalp_filtered(category):
                qs = HairProduct.objects.filter(category__icontains=category, vegan=vegan)
                if color_treated:
                    qs = qs.filter(sulfate_free__iexact='Yes')
                if price_range == "$":
                    return qs.filter(price__lte=12.00)
                elif price_range == "$$":
                    return qs.filter(price__gt=12.00, price__lte=25.00)
                else:
                    return qs.filter(price__gt=25.00)

            if scalp_condition == "oily":
                special_recommendations["Clarifying Shampoo (Use Weekly)"] = list(scalp_filtered("Clarifying"))

            elif scalp_condition == "flaky":
                special_recommendations["Scalp Oil (Use Daily)"] = list(scalp_filtered("Oil"))
                special_recommendations["Hair Mask (Use Weekly)"] = list(scalp_filtered("Mask"))

            elif scalp_condition == "in_between":
                special_recommendations["Clarifying Shampoo"] = list(scalp_filtered("Clarifying"))
                special_recommendations["Scalp Oil"] = list(scalp_filtered("Oil"))
                special_recommendations["Hair Mask"] = list(scalp_filtered("Mask"))

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

            try:
                routine_data = json.loads(routine_data_raw)
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