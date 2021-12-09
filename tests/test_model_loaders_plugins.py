import sys
sys.path.insert(0,'../')
import pprint

from ttr import ttr


def test_yangson_loader_custom_dir():
    gen = ttr()
    gen.load_models(models_dir="./YANG_Models_folder/", model_plugin="yangson")
    # pprint.pprint(gen.models_dict)
    # print(gen.models_dict["interface_model"].ascii_tree())
    assert "interface" in gen.models_dict
    assert isinstance(gen.models_dict["interface"].ascii_tree(), str)
    
# test_yangson_loader()


def test_yangson_loader_default_dir():
    gen = ttr()
    gen.load_models()
    # pprint.pprint(gen.models_dict)
    # print(gen.models_dict["interface_model"].ascii_tree())
    assert "interface" in gen.models_dict
    assert isinstance(gen.models_dict["interface"].ascii_tree(), str)
    assert "vrf" in gen.models_dict
    assert isinstance(gen.models_dict["vrf"].ascii_tree(), str)
    
# test_yangson_loader_default_dir()