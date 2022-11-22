from io import StringIO
import csv
import os

from django.test import TestCase
from django.core import management

from vessels.management.commands.import_vessels import (
    CSV_VESSEL_ID_HEADER, 
    CSV_RECEIVED_TIME_HEADER, 
    CSV_LATITUDE_HEADER, 
    CSV_LONGITUDE_HEADER
)

WRONG_HEADER = [
    CSV_VESSEL_ID_HEADER, 
    CSV_RECEIVED_TIME_HEADER,
    CSV_LATITUDE_HEADER
]

SAMPLE_HEADER = [
    CSV_VESSEL_ID_HEADER, 
    CSV_RECEIVED_TIME_HEADER,
    CSV_LATITUDE_HEADER,
    CSV_LONGITUDE_HEADER
]
SAMPLE_ROW = ['5291', '2017-11-10 05:43:07.000000',	'30.49617', '123.83863']

class ImportVesselsCommandTests(TestCase):
    def setUp(self) -> None:
        f = open('wrong_columns.csv', 'w')
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(WRONG_HEADER)
        # close the file
        f.close()

        f = open('sample.csv', 'w')
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(SAMPLE_HEADER)
        writer.writerow(SAMPLE_ROW)
        # close the file
        f.close()

        return super().setUp()

    def test_command(self):
        out = StringIO()
        err = StringIO()

        management.call_command('import_vessels', stdout=out, stderr= err)

        self.assertTrue("Missing CSV file path" in err.getvalue())

    def test_wrong_columns_command(self):
        out = StringIO()
        err = StringIO()

        management.call_command(
            'import_vessels', 
            file='./wrong_columns.csv',
            stdout=out,
            stderr=err
        )
        self.assertTrue("CSV Structure is wrong?" in err.getvalue())

    def test_import_command(self):
        out = StringIO()
        management.call_command('import_vessels', file='./sample.csv', stdout=out)
        
        self.assertTrue("Import done. Vessels in DB: 1" in out.getvalue())
    
    def tearDown(self) -> None:
        os.remove('wrong_columns.csv')
        os.remove('sample.csv')
        return super().tearDown()

    