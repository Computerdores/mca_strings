#!/bin/python3
from anvil import Region
from nbt import nbt
import argparse

found = set()

def harvest_region(file):
    region = Region.from_file(file)
    for x in range(32):
        for y in range(32):
            harvest_chunk(region.chunk_data(x,y))

def harvest_chunk(chunk: nbt.TAG_COMPOUND):
    if chunk == None:
        return
    for tag in chunk.tags:
        if tag.name == "Level":
            harvest_level(tag)

def harvest_level(level: nbt.TAG_COMPOUND):
    for tag in level.tags:
        if tag.id == 9 and tag.name == "TileEntities":
            harvest_tile_entities(tag)

def harvest_tile_entities(entities: nbt.TAG_COMPOUND):
    if len(entities.tags) != 0:
        for entity in entities.tags:
            if entity.id != 0:
                harvest_tile_entity(entity)

def harvest_tile_entity(entity: nbt.TAG_COMPOUND):
    id = entity.get("id").value
    x = entity.get('x').value
    y = entity.get('y').value
    z = entity.get('z').value
    if id == "minecraft:sign":
        print(f"Sign at {x} {y} {z}: {{")
        print(f"    {extract_sign_text(entity.get('Text1').value)}")
        print(f"    {extract_sign_text(entity.get('Text2').value)}")
        print(f"    {extract_sign_text(entity.get('Text3').value)}")
        print(f"    {extract_sign_text(entity.get('Text4').value)}")
        print(f"}}")
    else:
        print(f"Tile Entity at {x} {y} {z}: {{")
        harvest_tag(entity)
        print(f"}}")

def extract_sign_text(json: str):
    return json[9:-2]

def harvest_tag(tag: nbt.TAG):
    if tag == None:
        return
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
    parser = argparse.ArgumentParser(prog="mca_strings", description="Harvest all unique String Tags from a MC Region file.")
    parser.add_argument("region_file", type=argparse.FileType('rb'), nargs="+")
    for rf in parser.parse_args().region_file: #["regions/r.-1.-1.mca"]
        print(f"DEBUG: Region file: {rf.name}")
        harvest_region(rf)