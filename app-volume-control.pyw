from pynput import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


APPLICATION_NAMES = ['Spotify.exe', 'Amazon Music.exe']
VOLUME_STEP = 0.05

class AudioController:
    '''Class to control the audio of a list of applications
    Attributes:
    process_names: list of the names of the applications to control
    volume: the volume of the applications
    sys_volume_saved: the saved system volume
    sys_volume: the system volume interface
    '''
    def __init__(self, process_names: list[str]):
        '''Initializes the AudioController class
        Args:
        process_names: list of the names of the applications to control
        '''
        self.process_names = process_names
        self.volume = 1.0
        self.sys_volume_saved = 0.0
        self.sys_volume = self.get_sys_volume()

    def get_sys_volume(self):
        '''Returns the system volume interface'''
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return interface.QueryInterface(IAudioEndpointVolume)

    def decrease_volume(self, decibels: float):
        '''Decrease the application volume by decibels
        Args:
        decibels: the amount of decibels to decrease the volume by
        '''
        sessions = AudioUtilities.GetAllSessions()
        # 0.0 is the min value, lower by decibels
        self.volume = max(0.0, self.volume - decibels)
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() in self.process_names:
                interface.SetMasterVolume(self.volume, None)

    def increase_volume(self, decibels: float):
        '''Increase the application volume by decibels
        Args:
        decibels: the amount of decibels to increase the volume by
        '''
        sessions = AudioUtilities.GetAllSessions()
        # 1.0 is the max value, raise by decibels
        self.volume = min(1.0, self.volume + decibels)
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() in self.process_names:
                interface.SetMasterVolume(self.volume, None)

    def save_sys_volume(self):
        '''Saves the system volume for later restoration'''
        self.sys_volume_saved = self.sys_volume.GetMasterVolumeLevelScalar()

    def restore_sys_volume(self):
        '''Restores the system volume to the saved value'''
        self.sys_volume.SetMasterVolumeLevelScalar(self.sys_volume_saved, None)
    
    def unmute_sys_volume(self):
        '''Unmutes the system volume'''
        self.sys_volume.SetMute(0, None)

app_audio_controller = AudioController(APPLICATION_NAMES)
toggle_application_control = False

with keyboard.Events() as events:
    for event in events:
        # If the mute key is pressed, unmute the system volume and start controlling the applications volume
        if event.key == keyboard.Key.media_volume_mute:
            if isinstance(event, keyboard.Events.Press):
                app_audio_controller.save_sys_volume()
                toggle_application_control = not toggle_application_control
            app_audio_controller.unmute_sys_volume()
        elif toggle_application_control and isinstance(event,keyboard.Events.Release):
            # If the volume up or down key is pressed, increase or decrease the volume of the applications
            if event.key == keyboard.Key.media_volume_up:
                app_audio_controller.increase_volume(VOLUME_STEP)
                app_audio_controller.restore_sys_volume()
            if event.key == keyboard.Key.media_volume_down:
                app_audio_controller.decrease_volume(VOLUME_STEP)
                app_audio_controller.restore_sys_volume()
