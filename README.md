# PTZ_OBS_control
A small project to control a (Reolink) PTZ camera via OBS scene selection.

Introduction
Many Reolink cameras offer the option of RTMP or RTPS video stream output, which can be accessed by OBS (or other streaming software). Such a video stream has some latency, but it still has its uses. 
Most of Reolink's PTZ cameras can be controlled by HTTP(S) API commands. For instance, you can change the camera angle and zoom into one of 64 premade presets (that can be created in the Reolink app).
This allows one physical camera to show many predefined frames, which is useful, for instance, when the camera covers a large outdoor area or paddock.

There is a plugin for websocket control in the OBS software. This can read the states in OBS and make changes, such as changing the OBS scene that is going live.
The Python script works as an intermediary between the camera API and OBS websocket, so changing the OBS scene makes the camera change preset (changing the framing). This helps automate a live stream.

Link to Reolink API
https://community.reolink.com/topic/4196/reolink-camera-api-user-guide_v8-updated-in-april-2023

Link to OBS websocket project
https://github.com/obsproject/obs-websocket

## Getting Started

### Prerequisites computer running script and OBS
- Python 3.x installed
- OBS with the websocket plugin installed and configured
- The computer that runs the script / OBS software must be in the same local area network as the camera

### Python libraries required
pip install obswebsocket requests

### PTZ camera configuration
- you need the IP address of the PTZ camera (and login credentials)
- You have to have set a few presets in the PTZ camera app.
- HTTP has to be activated for the camera in the PTZ camera app.
- RTMP or RTPS output has to be activated for the camera in the PTZ camera app.
-   When RTMP or RTPS is activated, add the camera as a media source in OBS (rtsp://admin:secret@192.168.1.x:554/Preview_01_main)


Change the script to suit your needs, the IP address for the PTZ camera, the username/password for the PTZ, the password for the OBS websocket, and the OBS scene name used. 
Run the script (I use PowerShell). The script output contains some simple logging that shows whether the script can connect to OBS and the camera.




I plan to use this for a specific streaming project, 
I will add support for a secondary camera and some small improvements for connection stability.
But I don't think this will be something I will support or develop a lot further.
This script was based on example code from both projects, and I was helped greatly by AI (ChatGPT 4o) putting it together.
