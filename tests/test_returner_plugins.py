import sys
sys.path.insert(0,'../')
import pprint
import shutil
import os

from ttr import ttr

def test_file_returner_1():
    # delete previously generated results
    if os.path.exists("./Output/test_file_returner_1"):
        shutil.rmtree("./Output/test_file_returner_1")
    generator = ttr(
        "./mock_data/csv_data_1.csv", 
        returner="file", 
        returner_kwargs={
            "result_dir": "./Output/test_file_returner_1/"
        }
    )
    generator.run()
    with open("./Output/test_file_returner_1/r1.txt") as f:
        assert f.read() == """hostname r1
!
interface loopback0
  ip address 1.1.1.1/32"""
    with open("./Output/test_file_returner_1/r2.txt") as f:
        assert f.read() == ""
    with open("./Output/test_file_returner_1/r3.txt") as f:
        assert f.read() == ""   
        
def test_terminal_returner_1():
    generator = ttr(
        "./mock_data/csv_data_1.csv", 
        returner="terminal"
    )

# test_terminal_returner_1()
