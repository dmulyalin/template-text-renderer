import logging
import os


def dump(
        data_dict, 
        result_dir="./Output/",
        **kwargs
    ):
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    for datum_name, filedata in data_dict.items():
        filename = os.path.join(
            result_dir, "{}.txt".format(
                datum_name
            )
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(filedata)
