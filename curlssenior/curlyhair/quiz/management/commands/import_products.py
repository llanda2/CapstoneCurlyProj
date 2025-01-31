import csv
from django.core.management.base import BaseCommand
from quiz.models import HairProduct

class Command(BaseCommand):
    help = 'Import hair products from CSV'

    def handle(self, *args, **kwargs):
        with open('products.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check the 'Vegan?' field and convert to boolean
                vegan = row['Vegan?'].strip().lower() == 'yes'
                # Split multiple values in 'Curl Pattern' and 'Hair Type'
                curl_pattern = row['Curl Pattern']
                hair_type = row['Hair Type']
                weight = row['Weight (L,M,H)']
                helpful_areas = row['Helpful Areas']

                # Create and save the HairProduct instance
                product = HairProduct(
                    brand=row['Brand'],
                    name=row['Name'],
                    category=row['Category'],
                    price=row['Price'],
                    curl_pattern=curl_pattern,
                    hair_type=hair_type,
                    vegan=vegan,
                    weight=weight,
                    helpful_areas=helpful_areas
                )
                product.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported products'))
