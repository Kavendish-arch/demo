#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：AudioAPI.py
@Author  ：chenyingtao
@Date    ：2025/3/19 17:18 
"""

import re
import torch
import torchaudio
import numpy as np
from funasr import AutoModel
from remoteDeepSeek.remote import remote_infer as Remote_inferAI

import wave
"""
模型调用接口
"""
model = "iic/SenseVoiceSmall"
model = AutoModel(model=model,
                  vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                  vad_kwargs={"max_single_segment_time": 30000},
                  trust_remote_code=True,
                  )


def model_inference(input_wav, language, fs=16000):
    """
    Perform model inference on the input audio.

    Parameters:
    - input_wav: The input audio data, can be a tuple containing the sampling rate and audio data.
    - language: The language of the input audio, defaults to "auto".
    - fs: The sampling rate of the input audio, defaults to 16000.

    Returns:
    - text: The transcription result of the audio.
    """
    # Define language abbreviations for different languages
    language_abbr = {
        "auto": "auto", "zh": "zh", "en": "en", "yue": "yue", "ja": "ja", "ko": "ko",
        "nospeech": "nospeech"
    }

    # Set default language to "auto" if the provided language is empty
    language = "auto" if len(language) < 1 else language
    # Get the selected language abbreviation based on the provided language
    selected_language = language_abbr[language]

    # Check if the input audio is in the correct format and perform preprocessing if necessary
    if isinstance(input_wav, tuple):
        fs, input_wav = input_wav
        input_wav = input_wav.astype(np.float32) / np.iinfo(np.int16).max
        # Convert to mono if the audio is stereo
        if len(input_wav.shape) > 1:
            input_wav = input_wav.mean(-1)
        # Resample the audio to 16000Hz if the sampling rate is different
        if fs != 16000:
            print(f"audio_fs: {fs}")
            resampler = torchaudio.transforms.Resample(fs, 16000)
            input_wav_t = torch.from_numpy(input_wav).to(torch.float32)
            input_wav = resampler(input_wav_t[None, :])[0, :].numpy()

    # Decide whether to merge voice activity detection (VAD) segments based on the selected task
    merge_vad = True  # False if selected_task == "ASR" else True

    # Print the selected language and VAD merging setting
    print(f"language: {language}, merge_vad: {merge_vad}")
    # Generate the transcription result using the model
    text = model.generate(input=input_wav,
                          cache={},
                          language=language,
                          use_itn=True,
                          batch_size_s=60, merge_vad=merge_vad)

    # Print and process the generated transcription result
    # print(text)
    text = text[0]["text"]

    # Print the final processed transcription result
    # print(text)

    # Return the final transcription result
    return text


def read_audio_file(input_filename, fs=16000, channels=1):
    """
    Read an audio file and return the audio data as a NumPy array.

    Parameters:
    - input_filename: The filename of the audio file to read.
    - fs: The sampling rate of the audio.
    - channels: The number of audio channels (1 for mono, 2 for stereo).

    Returns:
    - input_wav: The audio data as a NumPy array.
    """
    # Open the WAV file for reading
    with wave.open(input_filename, 'rb') as wf:
        # Check if the file has the correct number of channels
        if wf.getnchannels() != channels:
            raise ValueError(f"Expected {channels} channels, but got {wf.getnchannels()} channels.")

        # Read all frames from the file
        frames = wf.readframes(wf.getnframes())
        # Convert the frames to a NumPy array
        input_wav = np.frombuffer(frames, dtype=np.int16)

        # Normalize the audio data to the range [-1, 1]
        input_wav = input_wav.astype(np.float32) / np.iinfo(np.int16).max

        # If the audio is stereo, convert it to mono
        if len(input_wav.shape) > 1:
            input_wav = input_wav.mean(-1)

        # Resample the audio to the desired sampling rate if necessary
        if wf.getframerate() != fs:
            resampler = torchaudio.transforms.Resample(wf.getframerate(), fs)
            input_wav_t = torch.from_numpy(input_wav).to(torch.float32)
            input_wav = resampler(input_wav_t[None, :])[0, :].numpy()

    return input_wav


def remove_bracketed_text(text):
    """
    Remove text within angle brackets and the brackets themselves.

    Parameters:
    - text: The input string containing text with angle brackets.

    Returns:
    - cleaned_text: The string with angle-bracketed text removed.
    """
    pattern = r'<\|.*?\|>'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


if __name__ == "__main__":
    # record_audio("audioWs/test.wav", duration=5)
    input_wav = read_audio_file("audioWs/output.wav")
    text = model_inference(input_wav, language="zh")
    print(f"Transcription: {text}")

    # 清理尖括号及其内容
    cleaned_text = remove_bracketed_text(text)

    answer = Remote_inferAI(cleaned_text)
    print(dict(answer)["content"])
