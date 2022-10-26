#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    VTT to JSON converter
    Author: Bart Deijkers
    Created: 2022-10-20

    Usage: python vtt2json.py --file_in <vtt|json file> --out_path <output path> --method <file|npostart>
'''

import argparse
import os
from pathlib import Path, PurePosixPath
import json
import requests
import os
import sys
import webvtt


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download and convert vtt subtitles to json format")
    parser.add_argument("--file_in", help="Input vtt file")
    parser.add_argument("--method", default="file", choices=[
                        "file", "npostart"], help="Determine the method to parse the data")
    parser.add_argument("--out_path", default="", help="output path")

    args = parser.parse_args()
    return args


def do_system(arg):
    print(f"==== running: {arg}")
    err = os.system(arg)
    if err:
        print("FATAL: command failed")
        sys.exit(err)

# Convert the subtitles


def vtt2json(filename):
    vtt_json = []
    for caption in webvtt.read(filename):
        start = caption.start.replace(".", "")[:-3]
        end = caption.end.replace(".", "")[:-3]
        vtt_json.append({"start": start, "end": end, "text": caption.text})
    return vtt_json


def get_vtt(id, url, out_path):
    try:
        # create subfolder for vtt files
        Path(out_path+"/vtt").mkdir(parents=True, exist_ok=True)

        # download vtt file
        response = requests.get(url)
        if response.status_code == 200:
            with open(out_path+"/vtt/"+id + ".vtt", "wb") as f:
                f.write(response.content)
                f.close()
                return True
        else:
            print("Error: " + str(response.status_code))
            return False
    except Exception as e:
        print(e)
        return False


def set_json(id, json_data, out_path):
    Path(out_path + "/json").mkdir(parents=True, exist_ok=True)
    with open(out_path + "/json/" + id + ".json", "w") as f:
        json.dump(json_data, f, indent=4)
        f.close()


# load npostart metadata json file and get id value from each item
def load_batch_npostart(json_data, out_path):
    with open(json_data, "r") as f:
        data = json.load(f)
        for item in data:
            id = item["id"]

            # get vtt file from url
            url = "https://assetscdn.npostart.nl/subtitles/original/nl/" + id + ".vtt"
            result = get_vtt(id, url, out_path)
            if result:
                json_data = vtt2json(out_path + "/vtt/" + id + ".vtt")
                set_json(id, json_data, out_path)
            else:
                print("Could not process subtitle ID: " + id)
        f.close()


if __name__ == "__main__":
    args = parse_args()

    if args.method == "" and args.file_in == "":
        print("Error: no input file and/or method specified")
        sys.exit(1)

    if args.file_in != "":
        if args.method == "npostart":
            load_batch_npostart(args.file_in, args.out_path)
        if args.method == "file":
            id = args.file_in.split(".")[0]
            json_data = vtt2json(args.file_in)
            set_json(id, json_data, args.out_path)       