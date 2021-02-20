import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr

def test_ttr_load_template_method_load_content_inline():
    template = """
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
    gen = ttr(data=data, data_plugin="yaml")
    gen.load_templates(template_name="interfaces.cisco_ios.txt", template_content=template)
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

# test_ttr_load_template_method_load_content_inline()

def test_ttr_base_to_dir_templates_loader():
    """
    gen.load_templates will fallback on using base template loader, which in turn will 
    fallback on using file template loader due to order of selection logic
    """
    gen = ttr(
        data="./mock_data/quick_start_mock_data.yaml"
    )
    gen.load_templates(template_name="interfaces.cisco_ios.txt", templates="./Templates/")
    # pprint.pprint(gen.templates_dict)
    assert gen.templates_dict == {'interfaces.cisco_ios.txt': 'interface {{ interface }}\n'
                                                              '{% if description is defined %}\n'
                                                              ' description {{ description }}\n'
                                                              '{% endif %}\n'
                                                              '{% if vid is defined %}\n'
                                                              ' encapsulation dot1q {{ vid }}\n'
                                                              '{% endif %}\n'
                                                              '{% if vrf is defined %}\n'
                                                              ' vrf forwarding  {{ vrf }}\n'
                                                              '{% endif %}\n'
                                                              '{% if ip is defined and mask is defined %}\n'
                                                              ' ip address {{ ip }} {{ mask }}\n'
                                                              '{% endif %}\n'
                                                              '{% if ipv6 is defined and maskv6 is defined %}\n'
                                                              ' ipv6 address {{ ipv6 }}/{{ maskv6 }}\n'
                                                              '{% endif %}\n'
                                                              ' exit\n'
                                                              '!'}
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
                               
# test_ttr_base_templates_loader()

def test_ttr_dir_templates_loader():
    gen = ttr(
        data="./mock_data/quick_start_mock_data.yaml"
    )
    gen.load_templates(template_name="interfaces.cisco_ios.txt", templates="./Templates/", plugin="dir")
    # pprint.pprint(gen.templates_dict)
    assert gen.templates_dict == {'interfaces.cisco_ios.txt': 'interface {{ interface }}\n'
                                                              '{% if description is defined %}\n'
                                                              ' description {{ description }}\n'
                                                              '{% endif %}\n'
                                                              '{% if vid is defined %}\n'
                                                              ' encapsulation dot1q {{ vid }}\n'
                                                              '{% endif %}\n'
                                                              '{% if vrf is defined %}\n'
                                                              ' vrf forwarding  {{ vrf }}\n'
                                                              '{% endif %}\n'
                                                              '{% if ip is defined and mask is defined %}\n'
                                                              ' ip address {{ ip }} {{ mask }}\n'
                                                              '{% endif %}\n'
                                                              '{% if ipv6 is defined and maskv6 is defined %}\n'
                                                              ' ipv6 address {{ ipv6 }}/{{ maskv6 }}\n'
                                                              '{% endif %}\n'
                                                              ' exit\n'
                                                              '!'}
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
                               
# test_ttr_dir_templates_loader()

def test_ttr_file_templates_loader_txt_file():
    gen = ttr(
        data="./mock_data/quick_start_mock_data.yaml"
    )
    gen.load_templates(template_name="./Templates/interfaces.cisco_ios.txt", plugin="file")
    # pprint.pprint(gen.templates_dict)
    assert gen.templates_dict == {'./Templates/interfaces.cisco_ios.txt': 'interface {{ interface }}\n'
                                                                          '{% if description is defined %}\n'
                                                                          ' description {{ description }}\n'
                                                                          '{% endif %}\n'
                                                                          '{% if vid is defined %}\n'
                                                                          ' encapsulation dot1q {{ vid }}\n'
                                                                          '{% endif %}\n'
                                                                          '{% if vrf is defined %}\n'
                                                                          ' vrf forwarding  {{ vrf }}\n'
                                                                          '{% endif %}\n'
                                                                          '{% if ip is defined and mask is defined %}\n'
                                                                          ' ip address {{ ip }} {{ mask }}\n'
                                                                          '{% endif %}\n'
                                                                          '{% if ipv6 is defined and maskv6 is defined %}\n'
                                                                          ' ipv6 address {{ ipv6 }}/{{ maskv6 }}\n'
                                                                          '{% endif %}\n'
                                                                          ' exit\n'
                                                                          '!'}
                               
# test_ttr_file_templates_loader()

def test_ttr_xlsx_templates_loader():
    gen = ttr(
        data="./mock_data/yaml_data_2.yaml",
        templates="./Templates/test_templates_file_1.xlsx"
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
    # pprint.pprint(gen.templates_dict)
    assert gen.templates_dict == {'interfaces.cisco_ios': 'interface {{ interface }}\n'
                                                          '{% if description is defined %}\n'
                                                          ' description {{ description }}\n'
                                                          '{% endif %}\n'
                                                          '{% if vid is defined %}\n'
                                                          ' encapsulation dot1q {{ vid }}\n'
                                                          '{% endif %}\n'
                                                          '{% if vrf is defined %}\n'
                                                          ' vrf forwarding  {{ vrf }}\n'
                                                          '{% endif %}\n'
                                                          '{% if ip is defined and mask is defined %}\n'
                                                          ' ip address {{ ip }} {{ mask }}\n'
                                                          '{% endif %}\n'
                                                          '{% if ipv6 is defined and maskv6 is defined %}\n'
                                                          ' ipv6 address {{ ipv6 }}/{{ maskv6 }}\n'
                                                          '{% endif %}\n'
                                                          ' exit\n'
                                                          '!'}
                               
# test_ttr_xlsx_templates_loader()

def test_ttr_xlsx_templates_loader_using_load_templates_method_base_plugin():
    gen = ttr(
        data="./mock_data/yaml_data_2.yaml"
    )
    gen.load_templates(
        templates="./Templates/test_templates_file_1.xlsx"
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
    # pprint.pprint(gen.templates_dict)
    assert gen.templates_dict == {'interfaces.cisco_ios': 'interface {{ interface }}\n'
                                                          '{% if description is defined %}\n'
                                                          ' description {{ description }}\n'
                                                          '{% endif %}\n'
                                                          '{% if vid is defined %}\n'
                                                          ' encapsulation dot1q {{ vid }}\n'
                                                          '{% endif %}\n'
                                                          '{% if vrf is defined %}\n'
                                                          ' vrf forwarding  {{ vrf }}\n'
                                                          '{% endif %}\n'
                                                          '{% if ip is defined and mask is defined %}\n'
                                                          ' ip address {{ ip }} {{ mask }}\n'
                                                          '{% endif %}\n'
                                                          '{% if ipv6 is defined and maskv6 is defined %}\n'
                                                          ' ipv6 address {{ ipv6 }}/{{ maskv6 }}\n'
                                                          '{% endif %}\n'
                                                          ' exit\n'
                                                          '!'}
                                                          
# test_ttr_xlsx_templates_loader_using_load_templates_method_base_plugin()


def test_ttr_xlsx_templates_loader_using_load_templates_method():
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  template: interfaces.cisco_ios
  device: rt-1
- interface: Gi1/2
  description: Customer C
  vid: 300
  ip: 10.0.3.1
  mask: 255.255.255.0
  vrf: cust_c
  template: interfaces.cisco_ios
  device: rt-1
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  template: interfaces.cisco_ios
  device: rt-2
"""

    gen = ttr(
        data=data, data_plugin="yaml"
    )
    gen.load_templates(
        templates="./Templates/test_templates_file_1.xlsx",
        templates_plugin="xlsx"
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
    # pprint.pprint(gen.templates_dict)
    assert gen.templates_dict == {'interfaces.cisco_ios': 'interface {{ interface }}\n'
                                                          '{% if description is defined %}\n'
                                                          ' description {{ description }}\n'
                                                          '{% endif %}\n'
                                                          '{% if vid is defined %}\n'
                                                          ' encapsulation dot1q {{ vid }}\n'
                                                          '{% endif %}\n'
                                                          '{% if vrf is defined %}\n'
                                                          ' vrf forwarding  {{ vrf }}\n'
                                                          '{% endif %}\n'
                                                          '{% if ip is defined and mask is defined %}\n'
                                                          ' ip address {{ ip }} {{ mask }}\n'
                                                          '{% endif %}\n'
                                                          '{% if ipv6 is defined and maskv6 is defined %}\n'
                                                          ' ipv6 address {{ ipv6 }}/{{ maskv6 }}\n'
                                                          '{% endif %}\n'
                                                          ' exit\n'
                                                          '!'}
                                                          
# test_ttr_xlsx_templates_loader_using_load_templates_method()