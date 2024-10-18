# application volume control
Small Background Script to control the volume of specified applications on your windows PC with the volume wheel on your keyboard.

## Install
### Install Python
https://www.python.org/downloads/
This script is currently compatible with versions < 3.13 because of its depedency to comtypes

### Install the Dependencies
```
pip install -r requirements.txt
```

## Configuration
Specify the targeted applications and the volume step for the wheel at the top of the script:
```
APPLICATION_NAMES = ['Spotify.exe', 'Amazon Music.exe']
VOLUME_STEP = 0.05
```

## Usage
Per default the system volume is controlled by the wheel.
Press the mute key on your keyboard to activate the application specific volume controls
