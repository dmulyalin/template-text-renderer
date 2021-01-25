import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr

def test_context_manager_1():
    with ttr("./mock_data/csv_data_1.csv") as g:
        assert g.data_loaded == [
            {'device': 'r1', 'hostname': 'r1', 'lo0_ip': '1.1.1.1', 'template': 'foo'},
            {'device': 'r2', 'hostname': 'r2', 'lo0_ip': '2.2.2.2', 'template': 'bar'},
            {'device': 'r3', 'hostname': 'r3', 'lo0_ip': '3.3.3.3', 'template': 'foobar'}
        ]
        results = g.run()
        assert results == {'r1': 'hostname r1\n!\ninterface loopback0\n  ip address 1.1.1.1/32',
                'r2': '',
                'r3': ''}