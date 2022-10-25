#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    parser.add_argument("--file_in", required="true", help="Input vtt file")
    parser.add_argument("--batch_in", default="meta.json",
                        help="Specify the url of the file to parse")
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


def get_vtt(id, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(id + ".vtt", "wb") as f:
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
    with open(out_path + id + ".json", "w") as f:
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
            result = get_vtt(id, url)
            if result:
                json_data = vtt2json(id + ".vtt")
                set_json(id, json_data, out_path)
            else:
                print("Error with subtitle ID: " + id)
        f.close()        


if __name__ == "__main__":
    args = parse_args()
    if args.batch_in != "":
        if args.method == "npostart":
            load_batch_npostart(args.batch_in, args.out_path)

    if args.method == "file":
        id = args.file_in.split(".")[0]
        json_data = vtt2json(args.file_in)
        set_json(id, json_data, args.out_path)
