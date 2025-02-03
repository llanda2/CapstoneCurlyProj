import os
import csv
from django.core.management.base import BaseCommand
from quiz.models import HairProduct

class Command(BaseCommand):
    help = 'Load hair products from CSV file'

    def handle(self, *args, **kwargs):
        # Directly use the absolute path
        csv_file = '/Users/laurenlanda/PycharmProjects/CapstoneCurlyProj/curlssenior/curlyhair/quiz/data/products.csv'

        # Check if the file exists
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        # Open and read the CSV file
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                HairProduct.objects.create(
                    brand=row['Brand'],
                    name=row['Name'],
                    category=row['Category'],
                    price=row['Price'],
                    curl_pattern=row['Curl Pattern'],
                    hair_type=row['Hair Type'],
                    vegan=row['Vegan?'].strip().lower() == 'yes',
                    weight=row['Weight (L,M,H)'],
                    helpful_areas=row['Helpful Areas']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))
