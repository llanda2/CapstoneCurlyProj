import os
import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from quiz.models import HairProduct


class Command(BaseCommand):
    help = 'Load hair products from CSV file'

    def handle(self, *args, **kwargs):
        # Absolute path to the CSV file
        csv_file = '/Users/laurenlanda/PycharmProjects/CapstoneCurlyProj/curlssenior/curlyhair/quiz/data/products.csv'

        # Check if the file exists
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        # Open and read the CSV file
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle missing or malformed data
                price = Decimal(row['Price'].strip()) if row['Price'].strip() else Decimal('0.00')

                # Ensure hold_level is valid (light, medium, strong) or set to None
                valid_hold_levels = {'light', 'medium', 'strong'}
                hold_level = row['Hold Level'].strip().lower() if row[
                                                                      'Hold Level'].strip().lower() in valid_hold_levels else None

                HairProduct.objects.get_or_create(
                    brand=row['Brand'].strip(),
                    name=row['Name'].strip(),
                    category=row['Category'].strip(),
                    price=price,
                    curl_pattern=row['Curl Pattern'].strip(),
                    hair_type=row['Hair Type'].strip(),
                    vegan=row['Vegan?'].strip().lower() == 'yes',
                    weight=row['Weight (L,M,H)'].strip(),
                    growth_areas=row.get('Growth Areas', '').strip(),  # Default empty if missing
                    sulfate_free=row['Sulfate Free?'].strip().lower() == 'yes',
                    hold_level=hold_level  # Now properly stores categorical values or None
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))
