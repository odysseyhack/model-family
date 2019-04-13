from iota import Iota
from iota.adapter.sandbox import SandboxAdapter
from iota.transaction import ProposedTransaction
from iota import Tag
from iota import TryteString
from iota import Address


# Define a sandbox api
def generate_api():
    return Iota(
        adapter = SandboxAdapter(
            uri = 'https://nodes.devnet.iota.org:443',
            auth_token = None
        ),
        seed='9JJCOGBBWONXNV9TEVCQQMKYIGKBBSJZOSXEWQEPIRYPYLQYBCUDHKFKSLRW9HZKALHUYXDLVETTDIMFD'
    )


# Anchor the event that describes a change in building data
def anchor_building_block(api, building_address, tag, message_string):
    message = TryteString.from_string(message_string)
    result = api.send_transfer(
        transfers=[
            ProposedTransaction(
                address=building_address,
                value=0,
                tag=tag,
                message=message
            )
        ]
    )
    return result


# Generate tag hash based on group id and group name
def generate_tag(group_id, group_name):
    return Tag(TryteString.from_string('{id}-{name}'.format(id=group_id, name=group_name)))


# Retrieve all anchors for a given building
def get_anchored_building_blocks(api, building_address):
    transactions = api.find_transactions(addresses=[Address(building_address)])
    return transactions


# Retrieve all anchored blocks for a given building
def get_anchored_building_blocks_by_group(api, building_address, group):
    # tag = generate_tag(group)
    transactions = api.find_transactions(addresses=[Address(building_address)])
    return transactions


# Simple test to write a static case into the tangle
def test_write():
    api = generate_api()
    address = api.get_new_addresses()['addresses'][0]
    tag = generate_tag(1, 'lifecycle')
    result = anchor_building_block(api, address, tag, 'created')
    return result


# Simple test to read an item from the tangle
def test_read():
    api = generate_api()
    address = api.get_new_addresses()['addresses'][0]
    result = get_anchored_building_blocks(api, address)
    return result
