"""
This script is licensed under GNU GPL v3.0 license: https://www.gnu.org/licenses/gpl-3.0.en.html

This script uses the https://www.geoplugin.com/ API.
Check their page to learn about usage limitations: https://www.geoplugin.com/aup
"""

import csv
import time
from urllib.request import urlopen
import json
import random
import argparse


def main(input_file_name, output_file_name):
    ip_list = get_ip_list(input_file_name)

    ip_with_add_info = []

    for ip in ip_list:
        json_data = get_data_from_geoplugin(ip[0])
        ip_info_array = [ip[0], json_data['geoplugin_city'], json_data['geoplugin_countryName']]
        ip_with_add_info.append(ip_info_array)

        time_step = random.uniform(0.0, 2.0)
        print("Got information about " + ip[0] + ". Waiting " + str(1.0 + time_step) + " seconds for next one")
        time.sleep(1.0 + time_step)

    write_output_file(output_file_name, ip_with_add_info)


def get_data_from_geoplugin(ip):
    try:
        api_url = "http://www.geoplugin.net/json.gp?ip="
        url = api_url + ip[0]
        response = urlopen(url)
        return json.loads(response.read())
    except:
        print("Error accessing geoPlugin API")
        exit(-1)


def get_ip_list(filename):
    try:
        file = open(filename, 'r')
        reader = csv.reader(file)
        ip_list = list(reader)
        file.close()
        return ip_list
    except:
        print("File " + filename + " doesn't exist or cannot be parsed")
        exit(-1)


def write_output_file(filename, ip_with_add_info):
    # dump the array to csv
    with open(filename, "w", newline="\n", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(ip_with_add_info)


args_parser = argparse.ArgumentParser(description="This script takes a list of IP addresses from a text file, each "
                                                  "on a new line, and returns the city and country of origin. It uses "
                                                  "the geoPlugin API.")
args_parser.add_argument("-i", "--input", help="Specifies the input file. Default \"in.txt\"", default="in.txt")
args_parser.add_argument("-o", "--output", help="Specifies the output file. Default \"out.csv\"", default="out.csv")
args = args_parser.parse_args()

main(args.input, args.output)
