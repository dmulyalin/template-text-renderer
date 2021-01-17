import logging

def dump(data_dict, **kwargs):
    for key, value in data_dict.items():
        print("""
# ---------------------------------------------------------------------------
# {} rendering results
# ---------------------------------------------------------------------------""".format(key))
        print(value)