#!/usr/bin/env python3

import sys
import time
import logging
import requests
from obswebsocket import obsws, events

# OBS WebSocket Settings
host = "localhost"
port = 4455
password = "password"

# PTZ Camera Settings for multiple cameras
CAMERAS = {
    "Camera1": {
        "IP": "192.168.1.x",
        "USER": "username",
        "PASSWORD": "password"
    },
    "Camera2": {
        "IP": "192.168.1.x",
        "USER": "username",
        "PASSWORD": "password"
    }
    # Add more cameras as needed
}

# Map scenes to PTZ presets and camera
SCENE_TO_PRESET = {
    "Kam1A-S01": {"camera": "Camera1", "preset_id": 1},
    "Kam1A-S02": {"camera": "Camera1", "preset_id": 2},
    "Kam2A-S01": {"camera": "Camera2", "preset_id": 0},
    "Kam2A-S02": {"camera": "Camera2", "preset_id": 1},
    # Add more scenes, cameras, and their corresponding preset IDs
}

logging.basicConfig(level=logging.DEBUG)

def set_ptz_preset(camera_name, preset_id):
    camera = CAMERAS.get(camera_name)
    if not camera:
        print(f"Camera {camera_name} not found in configuration.")
        return
    
    PTZ_IP = camera["IP"]
    USER = camera["USER"]
    PASSWORD = camera["PASSWORD"]

    # API endpoint with credentials included in the URL
    PTZ_URL = f"http://{PTZ_IP}/api.cgi?cmd=PtzCtrl&user={USER}&password={PASSWORD}"
    
    # Data payload for the POST request
    data = [{
        "cmd": "PtzCtrl",
        "param": {
            "channel": 0,
            "op": "ToPos",
            "id": preset_id,
            "speed": 32  # Assuming a speed setting is required, adjust as needed
        }
    }]

    try:
        # Send a POST request to move the PTZ to a preset
        response = requests.post(PTZ_URL, json=data, verify=False)  # verify=False for testing, consider true for production
        response_json = response.json()  # Parse JSON response
        print("PTZ Command Response:\n", response_json)  # Print the response
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed:", e)
    except ValueError as e:
        print("Error decoding JSON:", e)

def on_event(message):
    print("Got message: {}".format(message))

def on_switch(message):
    scene_name = message.getSceneName()
    print("You changed the scene to {}".format(scene_name))
    if scene_name in SCENE_TO_PRESET:
        camera_info = SCENE_TO_PRESET[scene_name]
        camera_name = camera_info["camera"]
        preset_id = camera_info["preset_id"]
        print(f"Setting PTZ preset to {preset_id} for scene {scene_name} on camera {camera_name}")
        set_ptz_preset(camera_name, preset_id)
    else:
        print(f"No PTZ preset configured for scene {scene_name}")

ws = obsws(host, port, password)
ws.register(on_event)
ws.register(on_switch, events.SwitchScenes)
ws.register(on_switch, events.CurrentProgramSceneChanged)
ws.connect()

try:
    print("OBS WebSocket connected and listening for scene changes.")
    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Script interrupted by user.")

ws.disconnect()
