import datetime
import json
from django.utils import timezone
from vessels.pagination import ResultPagination
from vessels.serializers import LocationGeoPointSerializer
from rest_framework.test import APIClient
from django.test import TestCase
from vessels.models import Vessel, Location
from django.core.paginator import Paginator
from faker import Faker
from django.contrib.gis.geos import Point
from vessels.management.commands.import_vessels import DATE_FORMAT

class LocationApiTests(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        Faker.seed(0)
        self.client = APIClient()

        # create mock models 
        self.vessel = Vessel()
        self.vessel.vessel_id = 1337
        self.vessel.save()

        self.location1 = Location()
        self.location1.received_time_utc = datetime.datetime.now(tz=timezone.utc)
        self.location1.point = Point(float(self.faker.latitude()), float(self.faker.longitude()))
        self.location1.vessel = self.vessel
        self.location1.save()

        self.location2 = Location()
        self.location2.received_time_utc = datetime.datetime.now(tz=timezone.utc)
        self.location2.point = Point(float(self.faker.latitude()), float(self.faker.longitude()))
        self.location2.vessel = self.vessel
        self.location2.save()

        self.location3 = Location()
        self.location3.received_time_utc = datetime.datetime.now(tz=timezone.utc)
        self.location3.point = Point(float(self.faker.latitude()), float(self.faker.longitude()))
        self.location3.vessel = self.vessel
        self.location3.save()

        return super().setUp()

    def test_list_vessel_locations(self):
        response = self.client.get(f"/api/v1/vessels/{self.vessel.vessel_id}/locations/")
        self.assertEqual(response.status_code, 200)
        
        # the result is paginated 
        vessel_locations = Location.objects.filter(vessel__vessel_id=self.vessel.vessel_id)
        page_size = ResultPagination.page_size
        paginator = Paginator(
            vessel_locations,
            page_size
        )       
        
        serializer = LocationGeoPointSerializer(paginator.page(1), many=True)
        self.assertFalse('count' in response.data)
        self.assertTrue('links' in response.data)

        self.assertEqual(serializer.data, response.data['results'])
    
    def test_get_valid_vessel_location(self):
        response = self.client.get(f"/api/v1/vessels/{self.vessel.vessel_id}/locations/{self.location1.id}/")
        self.assertEqual(response.status_code, 200)
        serializer = LocationGeoPointSerializer(self.location1, many=False)
        self.assertEqual(serializer.data, response.data)
    
    def test_get_invalid_vessel_location(self):
        response = self.client.get(f"/api/v1/vessels/{self.vessel.vessel_id}/locations/999/")
        self.assertEqual(response.status_code, 404)

    def test_create_valid_vessel_location(self):
        payload = {
            'received_time_utc': '2022-11-10T05:37:47Z',
            'point': {
                'type': 'Point',
                'coordinates': [
                    12.8415,
                    30.480433
                ]
            }
        }
        response = self.client.post(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/",
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        created_location = response.data
        db_location = Location.objects.filter(id=created_location['id'])
        self.assertIsNotNone(db_location)
        vessel_locations = Location.objects.filter(vessel__vessel_id=self.vessel.vessel_id).count()
        self.assertEqual(vessel_locations, 4)
    
    def test_create_invalid_vessel_location(self):
        payload = {
            # missing date,
            'point': {
                'type': 'Point',
                'coordinates': [
                    12.8415,
                    30.480433
                ]
            }
        }
        response = self.client.post(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/",
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("received_time_utc" in response.data)
    
    def test_update_valid_vessel_location(self):
        payload = {
            'received_time_utc': '2023-11-10 05:43:07.000000',
            'point': {
                'type': 'Point',
                'coordinates': [
                    10,
                    20
                ]
            }
        }
        response = self.client.put(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/{self.location1.id}/",
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.location1.refresh_from_db()

        self.assertEqual(
            self.location1.received_time_utc.strftime(DATE_FORMAT),
            payload['received_time_utc']
        )
        self.assertEqual(self.location1.point.coords[0], payload['point']['coordinates'][0])
        self.assertEqual(self.location1.point.coords[1], payload['point']['coordinates'][1])

    def test_update_invalid_vessel_location(self):
        payload = {
            'point': {
                'type': 'Point',
                'coordinates': [
                    10,
                    20
                ]
            }
        }
        response = self.client.put(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/{self.location1.id}/",
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("received_time_utc" in response.data)

    def test_update_nonexistant_vessel_location(self):
        payload = {
            'point': {
                'type': 'Point',
                'coordinates': [
                    10,
                    20
                ]
            }
        }
        response = self.client.put(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/99999999/",
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'].code, 'not_found')
    
    def test_delete_valid_vessel_location(self):
        response = self.client.delete(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/{self.location3.id}/"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Location.objects.filter(id=self.location3.id).exists())
    
    def test_delete_nonexistant_vessel_location(self):
        response = self.client.delete(
            f"/api/v1/vessels/{self.vessel.vessel_id}/locations/99999999/"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.data)

    def test_csv_locations(self):
        response = self.client.get(
            f"/api/v1/vessels/csv"
        )
        self.assertEqual(response.status_code, 200)
        row = response.data['results'][0]
        vessel_id = row['vessel_id']
        print(vessel_id)
        vessel_exists = Vessel.objects.filter(vessel_id=vessel_id).exists()
        self.assertTrue(vessel_exists)