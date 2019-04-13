from django.test import TestCase

from hnp.client import Client


class TestHNPProject(TestCase):
    def setUp(self):
        super().setUp()
        # official demo api key
        self.hnp = Client("9a96c922-d586-4113-82c4-7994a008022a")
        # call_command('loaddata', 'hnp/fixtures/houses.json')

    def test_list_projects(self):
        self.hnp.get_list_projects()

    def test_build_project(self):
        self.hnp._build_details(project_id=3033)

    def test_get_project(self):
        self.assertRaises(AttributeError, self.hnp.get_project)

    def tearDown(self):
        super().tearDown()
        del self.hnp
