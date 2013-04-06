#!/usr/bin/python
"""
This continually polls xbmc servers to make sure they are playing
videos. If not, it will make them play what they are meant to play.
"""
import json
import requests
import time
import sys
import os

def get_status(address, username, password):
    url = "http://%s/jsonrpc" % (address,)
    status_request = json.dumps({"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1})
    result = requests.post(url, data=status_request, headers={'content-type': 'application/json'}, auth=(username, password))
    result = json.loads(result.text)
    retval = False
    for player in result["result"]:
        if player["type"] == "video":
            return True
    return False

def play_file(address, username, password, file):
    url = "http://%s/jsonrpc" % (address,)
    play_request = json.dumps({"jsonrpc": "2.0", "method": "Player.Open", "params": { "item": { "path": file } }, "id": 1 })
    result = requests.post(url, data=play_request, headers={'content-type': 'application/json'}, auth=(username, password))

def main():
    hostnames = os.getenv("XBMC_HOSTNAME").split(':')
    usernames = os.getenv("XBMC_USERNAME").split(':')
    passwords = os.getenv("XBMC_PASSWORD").split(':')
    files = os.getenv("XBMC_FILE").split(':')
    while True:
        for hostname, username, password, filename in zip(hostnames, usernames, passwords, files):
            try:
                if not get_status(hostname, username, password):
                    play_file(hostname, username, password, filename)
            except Exception as exc:
                print("Failed to connect to %s: %s" % (hostname, exc))
        time.sleep(60)

if __name__ == '__main__':
    main()