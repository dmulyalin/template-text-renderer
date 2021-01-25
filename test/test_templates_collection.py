import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr


def test_loading_template_from_collection():
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  template: ttr://interfaces.cisco_ios.txt
  device: rt-1
- interface: Gi1/2
  description: Customer C
  vid: 300
  ip: 10.0.3.1
  mask: 255.255.255.0
  vrf: cust_c
  template: ttr://interfaces.cisco_ios.txt
  device: rt-1
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  template: ttr://interfaces.cisco_ios.txt
  device: rt-2
    """
    generator = ttr(data=data, data_plugin="yaml")
    generator.run()
    # pprint.pprint(generator.results)
    assert generator.results == {'rt-1': 'interface Gi1/1\n'
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
         
# test_loading_template_from_collection()

def test_loading_template_from_collection_no_txt_extension():
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  template: ttr://interfaces.cisco_ios
  device: rt-1
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  template: ttr://interfaces.cisco_ios
  device: rt-2
    """
    generator = ttr(data=data, data_plugin="yaml")
    generator.run()
    # pprint.pprint(generator.results)
    assert generator.results == {'rt-1': 'interface Gi1/1\n'
                                         ' description Customer A\n'
                                         ' encapsulation dot1q 100\n'
                                         ' vrf forwarding  cust_a\n'
                                         ' ip address 10.0.0.1 255.255.255.0\n'
                                         ' exit\n'
                                         '!',
                                 'rt-2': 'interface Gi1/2\n'
                                         ' description Customer B\n'
                                         ' encapsulation dot1q 200\n'
                                         ' vrf forwarding  cust_b\n'
                                         ' ip address 10.0.2.1 255.255.255.0\n'
                                         ' exit\n'
                                         '!'}
         
# test_loading_template_from_collection_no_txt_extension()