from django.contrib.gis.geos import Point
from django.utils import timezone
import csv
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.core.cache import cache
from vessels.models import Location, Vessel

CSV_VESSEL_ID_HEADER = 'vessel_id'
CSV_RECEIVED_TIME_HEADER = 'received_time_utc'
CSV_LATITUDE_HEADER = 'latitude'
CSV_LONGITUDE_HEADER = 'longitude'

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f" 

class Command(BaseCommand):
    help = 'Imports vessels from a .csv file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='')

    def handle(self, *args, **options):
        if options['file'] == '':
            self.stderr.write('Missing CSV file path')
            return 

        csv_file_path = options['file']
        file = open(csv_file_path)
        csvreader = csv.reader(file)
        header_row = [r.strip() for r in next(csvreader)]  # gets trimmed header row

        # check csv columns 
        if not CSV_VESSEL_ID_HEADER in header_row \
            or not CSV_RECEIVED_TIME_HEADER in header_row \
            or not CSV_LATITUDE_HEADER in header_row \
            or not CSV_LONGITUDE_HEADER in header_row:
            self.stderr.write("CSV Structure is wrong?")
        else:
            # invalidate all caches 
            cache.clear()

            vessel_id_index = header_row.index('vessel_id')
            received_time_utc_index = header_row.index('received_time_utc')
            latitude_index = header_row.index('latitude')
            longitude_index = header_row.index('longitude')
            
            for row in csvreader:
                vessel, _ = Vessel.objects.get_or_create(
                    vessel_id=row[vessel_id_index],
                    defaults={
                        'vessel_id': row[vessel_id_index],
                    }
                )

                # insert or update the related location 

                location, _ = Location.objects.update_or_create(
                    received_time_utc= datetime.strptime(row[received_time_utc_index], DATE_FORMAT),
                    vessel= vessel,
                    defaults={
                        'vessel': vessel,
                        'received_time_utc': datetime.strptime(
                            row[received_time_utc_index], 
                            DATE_FORMAT
                        ),
                        'point': Point(float(row[longitude_index]), float(row[latitude_index]))
                    }
                )
            file.close()

            self.stdout.write(f"Import done. Vessels in DB: {Vessel.objects.count()}")