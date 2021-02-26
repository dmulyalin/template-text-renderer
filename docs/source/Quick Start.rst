Quick Start
###########

After installing TTR, simplest way to start using it is via CLI utility. For instance,
this file with data at ``/path/to/data.yaml``::

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

And this file with template at ``/path/to/templates_folder/interfaces.cisco_ios.txt``::

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

Could be combined using TTR by running this command::

    ttr --data /path/to/data.yaml --template /path/to/templates_folder/ --print
    
Printing this output to terminal screen::

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

.. note:: ``--templates`` argument should be a path to folder with templates 
    files within that folder/subfolders or path to ``.xlsx`` spreadsheet file with 
    templates or path to ``.txt`` file with single template content.

TTR can be used as a module instantiating TTR object and supplying it with required attributes::

    import pprint
    from ttr import ttr
    
    templates = {
    "interfaces.cisco_ios.txt": """
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
    
    pprint.pprint(results)
    
    # prints:
    # 
    # {'rt-1': '\n'
    #          'interface Gi1/1\n'
    #          ' description Customer A\n'
    #          ' encapsulation dot1q 100\n'
    #          ' vrf forwarding  cust_a\n'
    #          ' ip address 10.0.0.1 255.255.255.0\n'
    #          ' exit\n'
    #          '!\n'
    #          '\n'
    #          'interface Gi1/2\n'
    #          ' description Customer C\n'
    #          ' encapsulation dot1q 300\n'
    #          ' vrf forwarding  cust_c\n'
    #          ' ip address 10.0.3.1 255.255.255.0\n'
    #          ' exit\n'
    #          '!',
    #  'rt-2': '\n'
    #          'interface Gi1/2\n'
    #          ' description Customer B\n'
    #          ' encapsulation dot1q 200\n'
    #          ' vrf forwarding  cust_b\n'
    #          ' ip address 10.0.2.1 255.255.255.0\n'
    #          ' exit\n'
    #          '!'}
    
It is also possible to source templates and data from text files::

    import pprint
    from ttr import ttr
    
    gen = ttr(
        data="./data/data.yaml", 
        templates="./Templates/"
    )
    
    gen.run()
    pprint.pprint(gen.results)
    
    # prints:
    # 
    # {'rt-1': 'interface Gi1/1\n'
    #          ' description Customer A\n'
    #          ' encapsulation dot1q 100\n'
    #          ' vrf forwarding  cust_a\n'
    #          ' ip address 10.0.0.1 255.255.255.0\n'
    #          ' exit\n'
    #          '!\n'
    #          'interface Gi1/2\n'
    #          ' description Customer C\n'
    #          ' encapsulation dot1q 300\n'
    #          ' vrf forwarding  cust_c\n'
    #          ' ip address 10.0.3.1 255.255.255.0\n'
    #          ' exit\n'
    #          '!',
    #  'rt-2': 'interface Gi1/2\n'
    #          ' description Customer B\n'
    #          ' encapsulation dot1q 200\n'
    #          ' vrf forwarding  cust_b\n'
    #          ' ip address 10.0.2.1 255.255.255.0\n'
    #          ' exit\n'
    #          '!'}
    
Data is the same as in previous example but stored in ``./data/data.yaml`` file, TTR picked up ``YAML`` loader based on data file extension. Directory ``./Templates/`` contains ``interfaces.cisco_ios.txt`` template file.

Notice that rendering results also accessible using TTR object ``results`` property.

TTR also can be invoked using context manager::

    import pprint
    from ttr import ttr
    
    with ttr("./data/data.yaml") as gen:
        results = gen.run()
        
    pprint.pprint(gen.results)
    
Above example produces same results as before, ``templates_dir`` used with default value which is ``./Templates/``.