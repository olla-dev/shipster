from datetime import tzinfo
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from vessels.models import Location, Vessel

class Command(BaseCommand):
    help = 'Seeds the db with random data using faker'

    def add_arguments(self, parser):
        parser.add_argument('--vessels', type=int, default=1000)
        parser.add_argument('--locations-per-vessel', type=int, default=150000)

    def handle(self, *args, **options):
        faker = Faker()
        Faker.seed(0)

        nb_vessels = options['vessels']
        locations_per_vessel = options['locations_per_vessel']

        for nv in range(nb_vessels):
            print(f"Vessel {nv}/{nb_vessels}:")
            vessel = Vessel()
            vessel.vessel_id = faker.pyint()
            vessel.save()

            locations = []

            for nl in range(locations_per_vessel):
                location = Location()
                location.vessel = vessel
                location.received_time_utc = faker.date_time_this_year(tzinfo=timezone.utc)
                location.point = Point(float(faker.latitude()), float(faker.longitude()))
                
                locations.append(location)

                print(f"{nl}/{locations_per_vessel} - Location {location}")
            Location.objects.bulk_create(locations)
        self.stdout.write(f"DB Seed done. Vessels in DB: {Vessel.objects.count()}")