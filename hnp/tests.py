from django.test import TestCase

from niki.client import Client


class TestNikiProject(TestCase):
    def setUp(self):
        super().setUp()
        # official demo api key
        self.niki = Client("9a96c922-d586-4113-82c4-7994a008022a")
        # call_command('loaddata', 'niki/fixtures/houses.json')

    def test_list_projects(self):
        self.niki.get_list_projects()

    def test_build_project(self):
        self.niki._build_details(project_id=3033)

    def test_get_project(self):
        self.assertRaises(AttributeError, self.niki.get_project)

    def tearDown(self):
        super().tearDown()
        del self.niki
