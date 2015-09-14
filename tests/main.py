import os
import pytest
from ansible_nsot import inventory
from ansible_nsot import NSoTInventory

here = os.path.abspath(os.path.dirname(__file__))


class Params:
    def test_withold_command(self):
        with pytest.raises(SystemExit):
            inventory.parse_args('')

    def test_with_list(self):
        assert inventory.parse_args('--list').list_

    def test_with_host(self):
        assert inventory.parse_args('--host rtr.example.com').host

        # Do not allow left out hostname if --host
        with pytest.raises(SystemExit):
            inventory.parse_args('--host')

    def test_with_both(self):
        with pytest.raises(SystemExit):
            inventory.parse_args('--list --host rtr.example.com')

    def test_with_bad_option(self):
        with pytest.raises(SystemExit):
            inventory.parse_args('--list --foo')


class Inventory:
    def test_config_parse(self):
        config_path = '%s/example.yaml' % here
        os.environ['NSOT_INVENTORY_CONFIG'] = config_path
        client = NSoTInventory
        should_be = {
            'routers': {
                'query': 'deviceType=ROUTER',
                'vars': {'a': 'b'}
            }
        }
        assert client.groups == should_be.keys()
        assert client.config == should_be