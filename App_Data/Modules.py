import os
import math
import tkinter as tk
from tkinter import font
import re
import glob
import time
import json
import shutil

def start_time(timed_segment_name):
    start_time = time.time()
    time_dict = {"Name": timed_segment_name,
     "Time": start_time}
    return time_dict

def total_time(time_dict:dict):
    end_time = time.time()
    total_time = end_time - time_dict.get("Time")
    print(f"Total time for {time_dict.get("Name")}: {total_time}")