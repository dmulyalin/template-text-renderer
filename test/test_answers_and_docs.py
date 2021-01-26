import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr

def test_quick_start():
    templates = {"interfaces.cisco_ios.txt": """
interface {{ interface }}
{% if description is defined %}
 description {{ description }}
{% endif %}
{% if vid is defined %}
 encapsulation dot1q {{ vid }}
{% endif %}
{% if vrf is defined %}
 vrf forwarding  {{ vrf }}
{% endif %}
{% if ip is defined and mask is defined %}
 ip address {{ ip }} {{ mask }}
{% endif %}
{% if ipv6 is defined and maskv6 is defined %}
 ipv6 address {{ ipv6 }}/{{ maskv6 }}
{% endif %}
 exit
!
"""
}

    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  template: interfaces.cisco_ios.txt
  device: rt-1
- interface: Gi1/2
  description: Customer C
  vid: 300
  ip: 10.0.3.1
  mask: 255.255.255.0
  vrf: cust_c
  template: interfaces.cisco_ios.txt
  device: rt-1
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  template: interfaces.cisco_ios.txt
  device: rt-2
"""

    gen = ttr(data=data, data_plugin="yaml", templates_dict=templates)
    results = gen.run()    
    # pprint.pprint(results)
    assert results == {'rt-1': '\n'
                               'interface Gi1/1\n'
                               ' description Customer A\n'
                               ' encapsulation dot1q 100\n'
                               ' vrf forwarding  cust_a\n'
                               ' ip address 10.0.0.1 255.255.255.0\n'
                               ' exit\n'
                               '!\n'
                               '\n'
                               'interface Gi1/2\n'
                               ' description Customer C\n'
                               ' encapsulation dot1q 300\n'
                               ' vrf forwarding  cust_c\n'
                               ' ip address 10.0.3.1 255.255.255.0\n'
                               ' exit\n'
                               '!',
                       'rt-2': '\n'
                               'interface Gi1/2\n'
                               ' description Customer B\n'
                               ' encapsulation dot1q 200\n'
                               ' vrf forwarding  cust_b\n'
                               ' ip address 10.0.2.1 255.255.255.0\n'
                               ' exit\n'
                               '!'}

# test_quick_start()

def test_quick_start_from_files():
    gen = ttr(
        data="./mock_data/quick_start_mock_data.yaml", 
        templates_dir="./Templates/"
    )
    gen.run()
    results = gen.results
    # pprint.pprint(results)
    assert results == {'rt-1': 'interface Gi1/1\n'
                               ' description Customer A\n'
                               ' encapsulation dot1q 100\n'
                               ' vrf forwarding  cust_a\n'
                               ' ip address 10.0.0.1 255.255.255.0\n'
                               ' exit\n'
                               '!\n'
                               'interface Gi1/2\n'
                               ' description Customer C\n'
                               ' encapsulation dot1q 300\n'
                               ' vrf forwarding  cust_c\n'
                               ' ip address 10.0.3.1 255.255.255.0\n'
                               ' exit\n'
                               '!',
                       'rt-2': 'interface Gi1/2\n'
                               ' description Customer B\n'
                               ' encapsulation dot1q 200\n'
                               ' vrf forwarding  cust_b\n'
                               ' ip address 10.0.2.1 255.255.255.0\n'
                               ' exit\n'
                               '!'}

# test_quick_start_from_files()

def test_quick_start_from_files_context_manager():
    with ttr("./mock_data/quick_start_mock_data.yaml") as gen:
        results = gen.run()
    # pprint.pprint(results)
    assert results == {'rt-1': 'interface Gi1/1\n'
                               ' description Customer A\n'
                               ' encapsulation dot1q 100\n'
                               ' vrf forwarding  cust_a\n'
                               ' ip address 10.0.0.1 255.255.255.0\n'
                               ' exit\n'
                               '!\n'
                               'interface Gi1/2\n'
                               ' description Customer C\n'
                               ' encapsulation dot1q 300\n'
                               ' vrf forwarding  cust_c\n'
                               ' ip address 10.0.3.1 255.255.255.0\n'
                               ' exit\n'
                               '!',
                       'rt-2': 'interface Gi1/2\n'
                               ' description Customer B\n'
                               ' encapsulation dot1q 200\n'
                               ' vrf forwarding  cust_b\n'
                               ' ip address 10.0.2.1 255.255.255.0\n'
                               ' exit\n'
                               '!'}
                               
def test_xlsx_data_loader_example():
    gen = ttr("./mock_data/table_data_loader_docs_example.xlsx")
    assert gen.data_loaded == [{'device': 'rt1',
                                'interface': 'Gi1/1.100',
                                'ip': '10.0.0.1',
                                'mask': 24,
                                'template': 'ttr://simple/interface.cisco_ios.txt',
                                'vid': 100,
                                'vrf': 'MGMT'},
                               {'device': 'rt1',
                                'interface': 'Gi2/3',
                                'ip': '10.3.0.1',
                                'mask': 30,
                                'template': 'ttr://simple/interface.cisco_ios.txt',
                                'vid': None,
                                'vrf': 'CUST'},
                               {'device': 'sw23',
                                'interface': 'Vlan21',
                                'ip': '10.0.0.2',
                                'mask': 24,
                                'template': 'ttr://simple/interface.cisco_ios.txt',
                                'vid': None,
                                'vrf': 'MGMT'}]
    results = gen.run()
    assert results == {'rt1': 'interface Gi1/1.100\n'
                              ' encapsulation dot1q 100\n'
                              ' vrf forwarding  MGMT\n'
                              ' ip address 10.0.0.1 24\n'
                              ' exit\n'
                              '!\n'
                              'interface Gi2/3\n'
                              ' encapsulation dot1q None\n'
                              ' vrf forwarding  CUST\n'
                              ' ip address 10.3.0.1 30\n'
                              ' exit\n'
                              '!',
                       'sw23': 'interface Vlan21\n'
                               ' encapsulation dot1q None\n'
                               ' vrf forwarding  MGMT\n'
                               ' ip address 10.0.0.2 24\n'
                               ' exit\n'
                               '!'}
         
# test_xlsx_data_loader_example()

def test_xlsx_data_loader_example_multitemplate():
    gen = ttr("./mock_data/table_data_loader_docs_example_multitemplate.xlsx", processors=["multitemplate"])
    # pprint.pprint(gen.data_loaded)
    assert gen.data_loaded == [{'device': 'rt1',
                                'interface': 'Gi1/1',
                                'ip': '10.0.0.1',
                                'mask': 30,
                                'template': 'ttr://simple/interface.cisco_ios.txt'},
                               {'device': 'rt2',
                                'interface': 'Gi1',
                                'ip': '10.0.0.2',
                                'mask': 30,
                                'template': 'ttr://simple/interface.cisco_nxos.txt'},
                               {'device': 'rt3',
                                'interface': 'Gi2/3',
                                'ip': '10.3.0.1',
                                'mask': 30,
                                'template': 'ttr://simple/interface.cisco_ios.txt'},
                               {'device': 'rt4',
                                'interface': 'Gi3',
                                'ip': '10.3.0.2',
                                'mask': 30,
                                'template': 'ttr://simple/interface.cisco_nxos.txt'}]
    results = gen.run()
    # pprint.pprint(results)
    assert results == {'rt1': 'interface Gi1/1\n ip address 10.0.0.1 30\n exit\n!',
                       'rt2': 'interface Gi1\n  ip address 10.0.0.2/30\n  exit\n!',
                       'rt3': 'interface Gi2/3\n ip address 10.3.0.1 30\n exit\n!',
                       'rt4': 'interface Gi3\n  ip address 10.3.0.2/30\n  exit\n!'}
    
# test_xlsx_data_loader_example_multitemplate()
    