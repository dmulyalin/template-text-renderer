import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr

def test_jinja2_render_csv_1():
    generator = ttr("./mock_data/csv_data_1.csv")
    generator.run()
    # pprint.pprint(generator.results)
    assert generator.results == {'r1': 'hostname r1\n!\ninterface loopback0\n  ip address 1.1.1.1/32',
               'r2': '',
               'r3': ''}
               
# test_jinja2_render_csv_1()