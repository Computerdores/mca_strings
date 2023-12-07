#!/bin/python3
from anvil import Region
from nbt import nbt

found = set()

def harvest_region(path):
    region = Region.from_file(path)
    for x in range(32):
        for y in range(32):
            harvest_tag(region.chunk_data(x,y))

def harvest_tag(tag: nbt.TAG):
    if tag.id == 8:                     # String
        log_string(tag.name, tag.value)
    elif tag.id == 10 or tag.id == 9:   # Compound or List
        for t in tag.tags:
            harvest_tag(t)


def log_string(name, value):
    if not (name,value) in found:
        found.add((name,value))
        print(f"\"{name}\": \"{value}\"")

if __name__=="__main__":
    harvest_region("r.-1.0.mca")