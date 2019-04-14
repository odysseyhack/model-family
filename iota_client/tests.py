from django.test import TestCase
from iota_client import test_client
from iota import Iota, Address, Tag
from iota.adapter import MockAdapter


# Create your tests here.
class TestIotaTestClient(TestCase):
    def setUp(self):
        super().setUp()
        self.mock_adapter = MockAdapter()
        self.api = Iota('mock://')
        self.api = Iota(self.mock_adapter)

    def test_anchor_building_blocks(self):
        message = 'Some data proof to lock on the chain'
        self.mock_adapter.seed_response(
            'send_transfer',
            response={'message': 'test'})

        address = Address('JUST9A9MOCK9ADDRESS99999999')
        tag = Tag('JUST9A9MOCK9TAG99999999')
        test_client.anchor_building_block(
            self.api,
            address,
            tag,
            message)