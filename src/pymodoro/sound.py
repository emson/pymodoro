# src/pymodoro/sound.py
import os
import platform
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional, Dict, List


def _run_command_silently(command: list[str]) -> bool:
    """
    Execute a command silently and return success status.
    
    Returns True if command executed successfully, False otherwise.
    """
    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            timeout=3
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _get_platform_sound_options() -> Dict[str, Dict[str, List[str]]]:
    """
    Get platform-specific sound options with fallbacks.
    
    Returns a nested dict: {platform: {sound_type: [sound_names_in_priority_order]}}
    """
    return {
        "Darwin": {  # macOS
            "work_end": ["Glass", "Ping", "Basso", "Pop"],
            "break_end": ["Ping", "Glass", "Bottle", "Pop"], 
            "default": ["Basso", "Glass", "Ping", "Pop"]
        },
        "Linux": {
            "work_end": ["bell", "notification", "alert", "beep", "complete"],
            "break_end": ["notification", "bell", "message", "beep", "info"],
            "default": ["bell", "beep", "notification", "alert", "message"]
        },
        "Windows": {
            "work_end": ["SystemExclamation", "SystemAsterisk", "SystemQuestion"],
            "break_end": ["SystemAsterisk", "SystemExclamation", "SystemQuestion"], 
            "default": ["SystemAsterisk", "SystemExclamation", "SystemQuestion"]
        }
    }


def _get_system_sound_path(sound_name: str) -> Optional[str]:
    """Get the path to a system sound file if it exists."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
        return sound_path if Path(sound_path).exists() else None
    elif system == "Linux":
        # Common sound paths on Linux with various extensions
        sound_paths = [
            f"/usr/share/sounds/alsa/{sound_name}.wav",
            f"/usr/share/sounds/{sound_name}.wav",
            f"/usr/share/sounds/{sound_name}.ogg",
            f"/usr/share/sounds/ubuntu/stereo/{sound_name}.ogg",
            f"/usr/share/sounds/freedesktop/stereo/{sound_name}.oga",
            f"/usr/share/sounds/generic/{sound_name}.wav",
        ]
        for path in sound_paths:
            if Path(path).exists():
                return path
    
    return None


def _play_windows_sound(sound_name: str) -> bool:
    """Play Windows system sound using winsound."""
    try:
        import winsound
        
        sound_mapping = {
            "SystemExclamation": winsound.MB_ICONEXCLAMATION,
            "SystemAsterisk": winsound.MB_ICONASTERISK,
            "SystemQuestion": winsound.MB_ICONQUESTION,
            "SystemHand": winsound.MB_ICONHAND,
        }
        
        sound_type = sound_mapping.get(sound_name, winsound.MB_OK)
        winsound.MessageBeep(sound_type)
        return True
    except ImportError:
        return False


def _play_system_sound(sound_name: str) -> bool:
    """
    Attempt to play a system sound using platform-specific tools.
    
    Returns True if successful, False otherwise.
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        sound_path = _get_system_sound_path(sound_name)
        if sound_path:
            return _run_command_silently(["afplay", sound_path])
    
    elif system == "Linux":
        sound_path = _get_system_sound_path(sound_name)
        if sound_path:
            # Try different audio players in order of preference
            players = ["paplay", "aplay", "mpg123", "mpv", "ffplay"]
            for player in players:
                if _run_command_silently([player, sound_path]):
                    return True
    
    elif system == "Windows":
        return _play_windows_sound(sound_name)
    
    return False


def _play_terminal_bell() -> bool:
    """
    Fall back to terminal bell as last resort.
    
    Returns True (we can't really know if it worked).
    """
    sys.stderr.write("\a")
    sys.stderr.flush()
    return True


def _play_notification_sound_sync(sound_type: str = "default") -> bool:
    """
    Play a notification sound synchronously with multiple fallback options.
    
    Args:
        sound_type: Type of sound to play ('work_end', 'break_end', or 'default')
    
    Returns:
        True if any sound method was attempted, False if all failed.
    """
    system = platform.system()
    sound_options = _get_platform_sound_options()
    
    # Get platform-specific sound options, fallback to generic if platform not found
    platform_sounds = sound_options.get(system, sound_options.get("Darwin", {}))
    sound_names = platform_sounds.get(sound_type, platform_sounds.get("default", ["bell"]))
    
    # Try each sound option in priority order
    for sound_name in sound_names:
        if _play_system_sound(sound_name):
            return True
    
    # If we're on an unknown platform or all sounds failed, try any available sound
    if system not in sound_options:
        for platform_name, platform_data in sound_options.items():
            for sound_name in platform_data.get("default", []):
                if _play_system_sound(sound_name):
                    return True
    
    # Fall back to terminal bell as absolute last resort
    return _play_terminal_bell()


def play_notification_sound(sound_type: str = "default") -> bool:
    """
    Play a notification sound asynchronously to avoid blocking the UI.
    
    Args:
        sound_type: Type of sound to play ('work_end', 'break_end', or 'default')
    
    Returns:
        True (since we're playing asynchronously, we assume success)
    """
    def _play_async():
        _play_notification_sound_sync(sound_type)
    
    # Play sound in background thread to avoid blocking UI
    sound_thread = threading.Thread(target=_play_async, daemon=True)
    sound_thread.start()
    return True


def play_work_end() -> bool:
    """Play a sound to signify the end of a work session."""
    return play_notification_sound("work_end")


def play_break_end() -> bool:
    """Play a sound to signify the end of a break session."""
    return play_notification_sound("break_end")


def play_warning() -> bool:
    """Play a warning sound to notify user of approaching session end."""
    return play_notification_sound("default")
