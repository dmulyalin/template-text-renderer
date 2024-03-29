import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr


def test_csv_data_plugin_load_from_file():
    generator = ttr("./mock_data/csv_data_1.csv")
    assert generator.data_loaded == [
        {'device': 'r1', 'hostname': 'r1', 'lo0_ip': '1.1.1.1', 'template': 'foo'},
        {'device': 'r2', 'hostname': 'r2', 'lo0_ip': '2.2.2.2', 'template': 'bar'},
        {'device': 'r3', 'hostname': 'r3', 'lo0_ip': '3.3.3.3', 'template': 'foobar'}
    ]
    
# test_csv_data_plugin_load_from_file()


def test_openpyxl_data_plugin():
    generator = ttr("./mock_data/table_data_1.xlsx")
    # pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'device': 'r1', 'hostname': 'r1', 'lo0_ip': '1.1.1.1', 'template': 'foo'},
                                     {'device': 'r2', 'hostname': 'r2', 'lo0_ip': '2.2.2.2', 'template': 'bar'},
                                     {'device': 'r3', 'hostname': 'r3', 'lo0_ip': '3.3.3.3', 'template': 'foobar'}]
    
# test_openpyxl_data_plugin()


def test_openpyxl_data_plugin_multitab_table():
    generator = ttr("./mock_data/table_multitab_data_2.xlsx")
    pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'device': 'r1',
                'hostname': 'r1',
                'lo0_ip': '1.1.1.1',
                'template': 'test_path/device_base'},
               {'device': 'r2',
                'hostname': 'r2',
                'lo0_ip': '2.2.2.2',
                'template': 'test_path/device_base'},
               {'device': 'r1',
                'interface': '10.0.0.1/24',
                'ip': 'Eth1',
                'template': 'test_path/interf_cfg'},
               {'device': 'r1',
                'interface': '10.0.1.1/24',
                'ip': 'Eth2',
                'template': 'test_path/interf_cfg'}]
    print(generator.templates_dict)
    generator.run()
    print(generator.results)
    assert generator.results == {'r1': 'hostname r1\n!\ninterface loopback0\n  ip address 1.1.1.1/32\ninterface 10.0.0.1/24\n  ip address Eth1/32\ninterface 10.0.1.1/24\n  ip address Eth2/32', 'r2': 'hostname r2\n!\ninterface loopback0\n  ip address 2.2.2.2/32'}
    
# test_openpyxl_data_plugin_multitab_table()


def test_openpyxl_data_plugin_templates_in_table():
    generator = ttr("./mock_data/table_multitab_inline_templates_data_3.xlsx")
    # pprint.pprint(generator.templates_dict)
    assert generator.templates_dict == {'test_path/device_base': 'hostname {{ hostname }}\n'
                                                                 '!\n'
                                                                 'interface loopback0\n'
                                                                 '  ip address {{ lo0_ip }} 255.255.255.255',
                                        'test_path/interf_cfg': 'interface {{ interface }}\n'
                                                                '  ip address {{ ip }}'}
    # pprint.pprint(generator.data_loaded)                     
    assert generator.data_loaded == [{'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.1',
                                      'template': 'test_path/device_base'},
                                     {'device': 'r2',
                                      'hostname': 'r2',
                                      'lo0_ip': '2.2.2.2',
                                      'template': 'test_path/device_base'},
                                     {'device': 'r1',
                                      'interface': 'Eth1',
                                      'ip': '10.0.0.1/24',
                                      'template': 'test_path/interf_cfg'},
                                     {'device': 'r1',
                                      'interface': 'Eth2',
                                      'ip': '10.0.1.1/24',
                                      'template': 'test_path/interf_cfg'}]
    # pprint.pprint(generator.results)
    generator.run()
    assert generator.results == {'r1': 'hostname r1\n'
                                      '!\n'
                                      'interface loopback0\n'
                                      '  ip address 1.1.1.1 255.255.255.255\n'
                                      'interface Eth1\n'
                                      '  ip address 10.0.0.1/24\n'
                                      'interface Eth2\n'
                                      '  ip address 10.0.1.1/24',
                                'r2': 'hostname r2\n'
                                      '!\n'
                                      'interface loopback0\n'
                                      '  ip address 2.2.2.2 255.255.255.255'}
    
# test_openpyxl_data_plugin_templates_in_table()

def test_openpyxl_data_plugin_with_multitemplate_processor():
    generator = ttr("./mock_data/table_multiple_templates.xlsx", processors=["multitemplate"])
    # pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.1',
                                      'template': 'test_path/device_base'},
                                     {'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.11',
                                      'template': 'test_path/device_base_rollback'},
                                     {'device': 'r2',
                                      'hostname': 'r2',
                                      'lo0_ip': '2.2.2.2',
                                      'template': 'test_path/device_base'},
                                     {'device': 'r2',
                                      'hostname': 'r2',
                                      'lo0_ip': '2.2.2.22',
                                      'template': 'test_path/device_base_rollback'},
                                     {'device': 'r1',
                                      'interface': 'Eth1',
                                      'ip': '10.0.0.1',
                                      'mask': 24,
                                      'template': 'test_path/interf_cfg'},
                                     {'device': 'r2',
                                      'interface': 'Eth1',
                                      'ip': '10.0.0.2',
                                      'mask': 24,
                                      'template': 'test_path/interf_cfg_b'},
                                     {'device': 'r1',
                                      'interface': 'Eth2',
                                      'ip': '10.0.1.1',
                                      'mask': 24,
                                      'template': 'test_path/interf_cfg'},
                                     {'device': 'r2',
                                      'interface': 'Eth2',
                                      'ip': '10.0.1.2',
                                      'mask': 24,
                                      'template': 'test_path/interf_cfg_b'}]
    # pprint.pprint(generator.templates_dict)
    assert generator.templates_dict == {'test_path/device_base': 'hostname {{ hostname }}\n'
                                                                 '!\n'
                                                                 'interface loopback0\n'
                                                                 '  ip address {{ lo0_ip }} 255.255.255.255',
                                        'test_path/device_base_rollback': 'no hostname {{ hostname }}\n'
                                                                          '!\n'
                                                                          'no interface loopback0',
                                        'test_path/interf_cfg': 'interface {{ interface }}\n  ip address {{ ip }}',
                                        'test_path/interf_cfg_b': 'interface {{ interface }}\n'
                                                                  '  ip address {{ ip }} {{ mask }}'}
    generator.run()
    # pprint.pprint(generator.results)
    assert generator.results == {'r1': 'hostname r1\n'
                                       '!\n'
                                       'interface loopback0\n'
                                       '  ip address 1.1.1.1 255.255.255.255\n'
                                       'no hostname r1\n'
                                       '!\n'
                                       'no interface loopback0\n'
                                       'interface Eth1\n'
                                       '  ip address 10.0.0.1\n'
                                       'interface Eth2\n'
                                       '  ip address 10.0.1.1',
                                 'r2': 'hostname r2\n'
                                       '!\n'
                                       'interface loopback0\n'
                                       '  ip address 2.2.2.2 255.255.255.255\n'
                                       'no hostname r2\n'
                                       '!\n'
                                       'no interface loopback0\n'
                                       'interface Eth1\n'
                                       '  ip address 10.0.0.2 24\n'
                                       'interface Eth2\n'
                                       '  ip address 10.0.1.2 24'}
    
# test_openpyxl_data_plugin_with_multitemplate_processor()

def test_yaml_data_plugin_load_from_text():
    data = """
- interface: Gi1/1
  description: Customer A
  dot1q: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
- interface: Gi1/2
  description: Customer B
  dot1q: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
    """
    generator = ttr()
    generator.load_data(data, data_plugin="yaml")
    # pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'description': 'Customer A',
                                      'dot1q': 100,
                                      'interface': 'Gi1/1',
                                      'ip': '10.0.0.1',
                                      'mask': '255.255.255.0',
                                      'vrf': 'cust_a'},
                                     {'description': 'Customer B',
                                      'dot1q': 200,
                                      'interface': 'Gi1/2',
                                      'ip': '10.0.2.1',
                                      'mask': '255.255.255.0',
                                      'vrf': 'cust_b'}]
                                      
def test_yaml_data_plugin_load_from_file():
    generator = ttr("./mock_data/yaml_data_1.yaml")
    assert generator.data_loaded == [{'description': 'Customer A',
                                      'dot1q': 100,
                                      'interface': 'Gi1/1',
                                      'ip': '10.0.0.1',
                                      'mask': '255.255.255.0',
                                      'vrf': 'cust_a'},
                                     {'description': 'Customer B',
                                      'dot1q': 200,
                                      'interface': 'Gi1/2',
                                      'ip': '10.0.2.1',
                                      'mask': '255.255.255.0',
                                      'vrf': 'cust_b'}]
# test_yaml_data_plugin_load_from_file()

def test_openpyxl_data_plugin_with_templates_split_processor():
    generator = ttr("./mock_data/table_inline_templates_data_templates_split_test.xlsx", processors=["templates_split"])
    # pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.1',
                                      'template': 'test_path/device_base'},
                                      {'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.1',
                                      'template': 'bgp_base'},
                                      {'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.1',
                                      'template': 'ospf_base'},
                                      {'device': 'r2',
                                      'hostname': 'r2',
                                      'lo0_ip': '2.2.2.2',
                                      'template': 'test_path/device_base'},
                                      {'device': 'r2',
                                      'hostname': 'r2',
                                      'lo0_ip': '2.2.2.2',
                                      'template': 'ospf_base'}]
    generator.run()
    # pprint.pprint(generator.results)  
    assert generator.results == {'r1': 'hostname r1\n'
                                       '!\n'
                                       'interface loopback0\n'
                                       '  ip address 1.1.1.1 255.255.255.255\n'
                                       'router bgp 65500\n'
                                       ' log neighbor changes\n'
                                       ' router-id 1.1.1.1\n'
                                       '!\n'
                                       'router ospf 1\n'
                                       ' area 0 password 123456\n'
                                       ' router-id 1.1.1.1\n'
                                       '!',
                                   'r2': 'hostname r2\n'
                                       '!\n'
                                       'interface loopback0\n'
                                       '  ip address 2.2.2.2 255.255.255.255\n'
                                       'router ospf 1\n'
                                       ' area 0 password 123456\n'
                                       ' router-id 2.2.2.2\n'
                                       '!'}    
                                       
# test_openpyxl_data_plugin_with_templates_split_processor()

def test_openpyxl_data_plugin_with_templates_filtering_processor():
    generator = ttr(
        "./mock_data/table_inline_templates_data_filtering_test.xlsx", 
        processors=["filtering"],
        processors_kwargs={
            "filters": ["core1", "r[12]"]
        }
    )
    # pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'device': 'r1',
                                      'hostname': 'r1',
                                      'lo0_ip': '1.1.1.1',
                                      'template': 'test_path/device_base'},
                                     {'device': 'r2',
                                      'hostname': 'r2',
                                      'lo0_ip': '2.2.2.2',
                                      'template': 'test_path/device_base'},
                                     {'device': 'core1',
                                      'hostname': 'core1',
                                      'lo0_ip': '1.1.1.11',
                                      'template': 'test_path/device_base'}]

# test_openpyxl_data_plugin_with_templates_filtering_processor()

def test_openpyxl_data_plugin_with_multitemplate_processor_empty_header_cell():
    generator = ttr("./mock_data/table_multiple_templates_empty_headers.xlsx", processors=["multitemplate"])
    # pprint.pprint(generator.data_loaded)
    assert generator.data_loaded == [{'device': 'r1',
                                      'interface': 'Eth1',
                                      'ip': '10.0.0.1',
                                      'template': 'test_path/interf_cfg'},
                                     {'device': 'r2',
                                      'interface': 'Eth1',
                                      'ip': '10.0.0.2',
                                      'template': 'test_path/interf_cfg_b'},
                                     {'device': 'r1',
                                      'interface': 'Eth2',
                                      'ip': '10.0.1.1',
                                      'template': 'test_path/interf_cfg'},
                                     {'device': 'r2',
                                      'interface': 'Eth2',
                                      'ip': '10.0.1.2',
                                      'template': 'test_path/interf_cfg_b'}]
    # pprint.pprint(generator.templates_dict)
    assert generator.templates_dict == {'test_path/device_base': 'hostname {{ hostname }}\n'
                                                                 '!\n'
                                                                 'interface loopback0\n'
                                                                 '  ip address {{ lo0_ip }} 255.255.255.255',
                                        'test_path/device_base_rollback': 'no hostname {{ hostname }}\n'
                                                                          '!\n'
                                                                          'no interface loopback0',
                                        'test_path/interf_cfg': 'interface {{ interface }}\n  ip address {{ ip }}',
                                        'test_path/interf_cfg_b': 'interface {{ interface }}\n'
                                                                  '  ip address {{ ip }} {{ mask }}'}
    generator.run()
    # pprint.pprint(generator.results)
    assert generator.results == {'r1': 'interface Eth1\n'
                                       '  ip address 10.0.0.1\n'
                                       'interface Eth2\n'
                                       '  ip address 10.0.1.1',
                                 'r2': 'interface Eth1\n'
                                       '  ip address 10.0.0.2 \n'
                                       'interface Eth2\n'
                                       '  ip address 10.0.1.2 '}
                                                                       
# test_openpyxl_data_plugin_with_multitemplate_processor_empty_header_cell()