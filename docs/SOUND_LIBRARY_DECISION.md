# Sound Library Decision

**Date:** 2025-11-08
**Status:** Decided - Keep Custom Implementation

## Context

The project originally listed `playsound>=1.3.0` as a dependency, but this library was never actually used in the codebase. Instead, a custom platform-specific sound implementation was created in `src/pymodoro/sound.py`.

## Problem with playsound

The original playsound library has several critical issues:

- **Unmaintained**: Last updated in 2021, no active development
- **Incompatible**: Does not work with Python 3.12+
- **Buggy**: Numerous issues with file paths, MCI errors, cross-platform compatibility
- **Installation failures**: Many users report pip install failures
- **Removed from typeshed**: Python typing project removed it due to being unmaintained

## Alternatives Considered

### 1. playsound3 (Modern Fork)
- **Pros**: Actively maintained (Nov 2025), supports MP3/WAV, Python 3.10+
- **Cons**: Requires bundling audio files, new library with limited track record
- **Verdict**: Good option but unnecessary given our working solution

### 2. simpleaudio
- **Pros**: Cross-platform, low-latency, no Python dependencies
- **Cons**: WAV only, requires C compilation, needs system dependencies
- **Verdict**: Solid but adds complexity and installation requirements

### 3. audioplayer
- **Pros**: MP3/WAV support, full playback control
- **Cons**: Heavy platform dependencies (PyGObject, PyObjC), overkill for our needs
- **Verdict**: Too complex for simple notification sounds

### 4. pygame.mixer
- **Pros**: Very reliable, battle-tested, cross-platform
- **Cons**: Entire pygame library dependency, slow imports, overkill
- **Verdict**: Too heavy for a CLI timer application

### 5. sounddevice
- **Pros**: Professional-grade audio, NumPy integration
- **Cons**: Complex API, requires PortAudio binary, designed for audio processing
- **Verdict**: Not suitable for simple playback

### 6. Keep Custom Implementation ✅ **SELECTED**
- **Pros**:
  - Already implemented and working
  - Zero external dependencies
  - Uses native system sounds
  - Multiple fallback options per platform
  - Asynchronous playback with threading
  - No audio files to bundle
  - Easier user installation
- **Cons**:
  - More code to maintain (but already written)
  - Platform-specific logic (but well-organized)

## Decision

**Keep the custom implementation** and remove the unused `playsound` dependency.

### Rationale

1. **It Works**: The custom implementation is production-ready with proper error handling and fallbacks

2. **Zero Dependencies**: No external packages means:
   - No installation issues
   - No security vulnerabilities from dependencies
   - No maintenance burden from unmaintained packages
   - Easier for users to install

3. **System Sounds**: Using native system sounds provides:
   - Professional, OS-consistent audio
   - No need to bundle audio files
   - Smaller package size
   - Automatic volume/system audio integration

4. **Perfect Fit**: For a CLI Pomodoro timer, simple notification sounds are all that's needed - no advanced audio features required

5. **Reliability**: System commands (`afplay`, `paplay`, `winsound`) are stable and unlikely to break

## Implementation Details

The current implementation in `src/pymodoro/sound.py`:

**Platform Support:**
- **macOS**: Uses `afplay` with system sounds (Glass, Ping, Basso, Pop)
- **Linux**: Multiple fallbacks (`paplay`, `aplay`, `mpg123`, `mpv`, `ffplay`)
- **Windows**: Uses stdlib `winsound` module
- **Fallback**: Terminal bell character (`\a`)

**Features:**
- Asynchronous playback (daemon threads)
- Three sound types: work_end, break_end, warning
- Mute support
- Multiple sound options per platform
- Comprehensive error handling

## Action Taken

1. ✅ Removed `playsound>=1.3.0` from `pyproject.toml`
2. ✅ Kept custom implementation in `src/pymodoro/sound.py`
3. ✅ Documented decision in this file

## Future Considerations

If requirements change and we need features like:
- Custom audio file playback
- Volume control beyond system settings
- Audio recording
- Complex audio processing

Then reconsider:
- **playsound3** for simple MP3/WAV playback
- **simpleaudio** for low-latency WAV playback
- **pygame.mixer** if already using pygame for other features

For now, the custom implementation is the optimal solution.
