#!/bin/python3
# Created by Sensei-CHO
import sys
import requests


def enum(list, ip, port=80):
    url = f"http://{ip}:{port}/"
    try:
        r = requests.get(url)
        readlist = open(list, "r")
        filelist = readlist.read().splitlines()
        readlist.close()
    except requests.exceptions.ConnectionError:
        print("Connection refused. Check IP address or your device.")
        exit()
    except requests.exceptions.InvalidURL:
        print("Connection refused. Check IP address or your device.")
        exit()
    except FileNotFoundError:
        print(f"File {list} don't exist")
        exit()

    valid = []
    print(f"Starting Enumaration on {url}")
    for file in filelist:
        testurl = url + file
        r = requests.get(testurl)
        if r.status_code == 200:
            print(f"[+] {testurl} do not require login")
            valid.append(testurl)
        elif r.status_code == 401:
            print(f"[-] {testurl} require login")
        elif r.status_code == 404:
            print(f"[-] {testurl} don't exist")
        elif r.status_code == 403:
            print(f"[-] {testurl} unauthorized")
        else:
            print(f"[*] {testurl} returned status code {r.status_code}")

    print("\nNo login required:\n")
    for url in valid:
        print(f"[+] {url}")

if __name__ == "__main__":
    try:
        filelist = sys.argv[1]
        ip = sys.argv[2]
        port = sys.argv[3]
        enum(filelist, ip, port)
    except IndexError:
        print("usage: ApexisURLEnum.py <file list> <CAM-IP> <PORT>\nMissing arguments")
        exit(1)
