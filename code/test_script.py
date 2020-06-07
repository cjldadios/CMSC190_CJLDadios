
import os
import sys

sys.path.insert(0, os.path.abspath("") + "/components") 

from global_ops import *



cmd_list = [
    "py main.py my_drum_demo.wav tempo 70 test all_classes",
    "py main.py my_drum_demo.wav tempo 70 test simple_classes " \
        + "classes simple",
    "py main.py my_drum_demo.wav tempo 70 test common_classes " \
        + "remove uncommon blacklist stick bell " \
        + "whitelist bass snare tom floor hihat hihat-open " \
        + "crash ride"
]

for cmd in cmd_list:
    os.system(cmd)
    # os.system("cls")


ring()
ring()
ring()
ring()
ring()