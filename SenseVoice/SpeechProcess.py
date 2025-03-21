#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：SpeechProcess.py
@Author  ：chenyingtao
@Date    ：2025/3/19 17:23 
"""

"""

实现python 录音功能
"""
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyaudio
import wave

def record_audio(output_filename, duration=5, fs=16000, channels=1, chunk=1024):
    """
    Record audio from the default microphone and save it to a WAV file.

    Parameters:
    - output_filename: The filename to save the recorded audio.
    - duration: The duration of the recording in seconds.
    - fs: The sampling rate of the audio.
    - channels: The number of audio channels (1 for mono, 2 for stereo).
    - chunk: The number of frames per buffer.
    """
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open a stream for recording
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=fs,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    # Record audio data in chunks
    for _ in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))


"""

实现python 录音功能
"""
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def record_audio(output_filename, duration=5, fs=16000, channels=1, chunk=1024):
    """
    Record audio from the default microphone and save it to a WAV file.

    Parameters:
    - output_filename: The filename to save the recorded audio.
    - duration: The duration of the recording in seconds.
    - fs: The sampling rate of the audio.
    - channels: The number of audio channels (1 for mono, 2 for stereo).
    - chunk: The number of frames per buffer.
    """
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open a stream for recording
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=fs,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    # Record audio data in chunks
    for _ in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

def play_audio(input_filename, fs=16000, channels=1, chunk=1024):
    """
    Play an audio file using the default speaker.

    Parameters:
    - input_filename: The filename of the audio file to play.
    - fs: The sampling rate of the audio.
    - channels: The number of audio channels (1 for mono, 2 for stereo).
    - chunk: The number of frames per buffer.
    """
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the WAV file for reading
    with wave.open(input_filename, 'rb') as wf:
        # Open a stream for playing
        stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

        print("Playing...")

        # Read data in chunks and play it
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        print("Finished playing.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

    # Terminate PyAudio
    audio.terminate()




# Example usage
if __name__ == "__main__":
    # record_audio("audioWs/test.wav", duration=5)
    play_audio("audioWs/test.wav")

