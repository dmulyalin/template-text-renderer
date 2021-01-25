"""
Terminal Returner Plugin
************************

**Plugin Name:** ``terminal``

This plugin prints rendered result to terminal screen
applying minimal formating to improve readability.

For instance if these are rendering results::

    {'rt-1': 'interface Gi1/1\\n'
             ' description Customer A\\n'
             ' encapsulation dot1q 100\\n'
             ' vrf forwarding  cust_a\\n'
             ' ip address 10.0.0.1 255.255.255.0\\n'
             ' exit\\n'
             '!\\n'
             'interface Gi1/2\\n'
             ' description Customer C\\n'
             ' encapsulation dot1q 300\\n'
             ' vrf forwarding  cust_c\\n'
             ' ip address 10.0.3.1 255.255.255.0\\n'
             ' exit\\n'
             '!',
     'rt-2': 'interface Gi1/2\\n'
             ' description Customer B\\n'
             ' encapsulation dot1q 200\\n'
             ' vrf forwarding  cust_b\\n'
             ' ip address 10.0.2.1 255.255.255.0\\n'
             ' exit\\n'
             '!'}
					
Terminal returner will print to screen::

    # ---------------------------------------------------------------------------
    # rt-1 rendering results
    # ---------------------------------------------------------------------------
    interface Gi1/1
     description Customer A
     encapsulation dot1q 100
     vrf forwarding  cust_a
     ip address 10.0.0.1 255.255.255.0
     exit
    !
    interface Gi1/2
     description Customer C
     encapsulation dot1q 300
     vrf forwarding  cust_c
     ip address 10.0.3.1 255.255.255.0
     exit
    !
    
    # ---------------------------------------------------------------------------
    # rt-2 rendering results
    # ---------------------------------------------------------------------------
    interface Gi1/2
     description Customer B
     encapsulation dot1q 200
     vrf forwarding  cust_b
     ip address 10.0.2.1 255.255.255.0
     exit
    !
	
This returner useful for debugging or, for instance, when it is easier 
to copy produced results from terminal screen.
"""

def dump(data_dict, **kwargs):
    """
    This function prints results to terminal screen
    
    :param data_dict: (dict) dictionary keyed by ``result_name_key`` where 
                      values are rendered results string
    """
    for key, value in data_dict.items():
        print("""
# ---------------------------------------------------------------------------
# {} rendering results
# ---------------------------------------------------------------------------""".format(key))
        print(value)