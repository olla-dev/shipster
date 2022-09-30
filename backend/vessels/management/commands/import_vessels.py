from venv import create
from django.contrib.gis.geos import Point
import csv
from django.core.management.base import BaseCommand, CommandError
from vessels.models import Location, Vessel

class Command(BaseCommand):
    help = 'Imports vessels from a .csv file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        csv_file_path = options['file']
        file = open(csv_file_path)
        csvreader = csv.reader(file)

        # skip header row
        next(csvreader, None)
        
        for row in csvreader:
            vessel, created = Vessel.objects.get_or_create(
                vessel_id=row[0],
                defaults={
                    'vessel_id': row[0],
                }
            )

            # insert or update the related location 

            location, _ = Location.objects.update_or_create(
                received_time_utc= row[1],
                vessel= vessel,
                defaults={
                    'vessel': vessel,
                    'received_time_utc': row[1],
                    'geo_location': Point(float(row[2]), float(row[3]))
                }
            )
        file.close()

        print(f"Import done. Vessels in DB: {Vessel.objects.count()}")