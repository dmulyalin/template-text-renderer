import sys
sys.path.insert(0,'../')
import pprint
import pytest
import logging

from ttr import ttr

logging.basicConfig(level=logging.DEBUG)

def test_ttr_yang_validate_list_of_dict():
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  device: R1
  template: interfaces.cisco_ios
  model: interface
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  device: R2
  template: interfaces.cisco_ios
  model: interface
    """
    gen = ttr()
    gen.load_models(
        model_plugin="yangson"
    )
    gen.load_data(data=data, data_plugin="yaml")
    gen.run()
    # pprint.pprint(gen.results)
    assert gen.results == {'R1': 'interface Gi1/1\n'
       ' description Customer A\n'
       ' encapsulation dot1q 100\n'
       ' vrf forwarding  cust_a\n'
       ' ip address 10.0.0.1 255.255.255.0\n'
       ' exit\n'
       '!',
 'R2': 'interface Gi1/2\n'
       ' description Customer B\n'
       ' encapsulation dot1q 200\n'
       ' vrf forwarding  cust_b\n'
       ' ip address 10.0.2.1 255.255.255.0\n'
       ' exit\n'
       '!'}

# test_ttr_yang_validate_list_of_dict()


def test_ttr_yang_validate_mandatory_key_missing():
    """
    data below missing mandatory "device" key
    """
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  template: interfaces.cisco_ios
  model: interface
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  template: interfaces.cisco_ios
  model: interface
    """
    gen = ttr()
    gen.load_models(
        model_plugin="yangson"
    )
    with pytest.raises(RuntimeError):
        gen.load_data(data=data, data_plugin="yaml")
    
    
# test_ttr_yang_validate_mandatory_key_missing()


def test_ttr_yang_validate_wrong_value_type():
    """
    data below has non-integer value for vlan
    """
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100abc
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  device: R1
  template: interfaces.cisco_ios
  model: interface
- interface: Gi1/2
  description: Customer B
  vid: 200
  ip: 10.0.2.1
  mask: 255.255.255.0
  vrf: cust_b
  device: R2
  template: interfaces.cisco_ios
  model: interface
    """
    gen = ttr()
    gen.load_models(
        model_plugin="yangson"
    )
    with pytest.raises(RuntimeError):
        gen.load_data(data=data, data_plugin="yaml")
    
    
# test_ttr_yang_validate_wrong_value_type()


def test_ttr_yang_validate_multiple_models():
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  device: R1
  template: interfaces.cisco_ios
  model: interface
- interface: Gi1/2
  description: Customer B
  vrf_rt: 65101:123
  vrf_rd: 10.0.1.1
  vrf_name: cust_b
  device: R2
  template: cisco_ios.vrf
  model: vrf
    """
    gen = ttr()
    gen.load_models()
    gen.load_data(data=data, data_plugin="yaml")
    gen.run()
    # pprint.pprint(gen.results)
    assert gen.results == {'R1': 'interface Gi1/1\n'
       ' description Customer A\n'
       ' encapsulation dot1q 100\n'
       ' vrf forwarding  cust_a\n'
       ' ip address 10.0.0.1 255.255.255.0\n'
       ' exit\n'
       '!',
 'R2': 'vrf cust_b\n'
       ' rd 10.0.1.1\n'
       ' description Customer B\n'
       ' address-family ipv4 unicast\n'
       '   rt 65101:123 both\n'
       '!\n'
       'interface Gi1/2\n'
       ' vrf cust_b\n'
       '!'}

# test_ttr_yang_validate_multiple_models()


def test_ttr_yang_validate_no_explicit_load_models():
    data = """
- interface: Gi1/1
  description: Customer A
  vid: 100
  ip: 10.0.0.1
  mask: 255.255.255.0
  vrf: cust_a
  device: R1
  template: interfaces.cisco_ios
  model: interface
- interface: Gi1/2
  description: Customer B
  vrf_rt: 65101:123
  vrf_rd: 10.0.1.1
  vrf_name: cust_b
  device: R2
  template: cisco_ios.vrf
  model: vrf
    """
    gen = ttr()
    gen.load_data(data=data, data_plugin="yaml")
    res = gen.run()
    # pprint.pprint(gen.results)
    assert res == {'R1': 'interface Gi1/1\n'
       ' description Customer A\n'
       ' encapsulation dot1q 100\n'
       ' vrf forwarding  cust_a\n'
       ' ip address 10.0.0.1 255.255.255.0\n'
       ' exit\n'
       '!',
 'R2': 'vrf cust_b\n'
       ' rd 10.0.1.1\n'
       ' description Customer B\n'
       ' address-family ipv4 unicast\n'
       '   rt 65101:123 both\n'
       '!\n'
       'interface Gi1/2\n'
       ' vrf cust_b\n'
       '!'}

# test_ttr_yang_validate_no_explicit_load_models()


def test_ttr_yang_validate_excel_data():
    gen = ttr(data="./mock_data/table_data_2_with_models.xlsx")
    res = gen.run()
    assert "vrf" in gen.models_dict
    assert "interface" in gen.models_dict
    # pprint.pprint(res)
    assert res == {'r1': 'interface Lo1\n'
       ' description foo\n'
       ' ip address 1.1.1.1 255.255.255.255\n'
       ' exit\n'
       '!\n'
       'vrf foo\n'
       ' rd 65101:101\n'
       ' description vrf foo note\n'
       ' address-family ipv4 unicast\n'
       '   rt 65101:101 both\n'
       '!\n'
       'interface Lo1\n'
       ' vrf foo\n'
       '!',
 'r2': 'interface Lo2\n'
       ' description bar\n'
       ' ip address 2.2.2.2 255.255.255.255\n'
       ' exit\n'
       '!\n'
       'vrf bar\n'
       ' rd 65101:102\n'
       ' description vrf bar note\n'
       ' address-family ipv4 unicast\n'
       '   rt 65101:102 both\n'
       '!\n'
       'interface Lo2\n'
       ' vrf bar\n'
       '!'}
	   
# test_ttr_yang_validate_excel_data()