#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice
@File    ：gui.py
@Author  ：chenyingtao
@Date    ：2025/3/19 17:33
"""
import os.path
import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
from AudioAPI import read_audio_file, model_inference
from remoteDeepSeek.remote import remote_infer as Remote_AI_Infer
from config.key import temp_dir


class AudioApp:
    def __init__(self, root, model_inference):
        self.root = root
        self.root.title("SenseVoice")

        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None

        self.fs = 16000
        self.channels = 1
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.output_filename = os.path.join(temp_dir, "output.wav")
        self.temp_txt = ""
        self.create_widgets()

        self.model_inference = model_inference

    def create_widgets(self):
        # 录音按键
        self.record_button = tk.Button(self.root, text="录音", command=self.start_recording)
        self.record_button.pack(pady=10)

        # 停止录音按键
        self.stop_button = tk.Button(self.root, text="停止录音", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        # 推理按键
        self.inference_button = tk.Button(self.root, text="推理", command=self.perform_inference)
        self.inference_button.pack(pady=10)

        # 搜索质谱清言
        self.infer_RemoteAI_button = tk.Button(self.root, text="搜索质谱清言", command=self.searchAnswerFromZhipuAI)
        self.infer_RemoteAI_button.pack(pady=10)

        self.save_edit_button = tk.Button(self.root, text="保存编辑文本", command=self.save_edit_text)
        self.save_edit_button.pack(pady=10)

        # 输出文本框
        self.output_text = tk.Text(self.root, height=30, width=150)
        self.output_text.pack(pady=10)

        self.answer_text = tk.Text(self.root, height=30, width=150)
        self.answer_text.pack(pady=10)

    def start_recording(self):
        if self.recording:
            messagebox.showwarning("警告", "已经在录音中")
            return

        self.recording = True
        self.frames = []

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.fs,
                                      input=True,
                                      frames_per_buffer=self.chunk)

        print("Recording...")
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.inference_button.config(state=tk.DISABLED)

        self.record_audio()

    def record_audio(self):
        if not self.recording:
            # messagebox.showwarning("警告", "没有在录音")
            return

        data = self.stream.read(self.chunk)
        self.frames.append(data)

        self.root.after(self.chunk // self.fs * 1000, self.record_audio)

    def stop_recording(self):
        if not self.recording:
            # messagebox.showwarning("警告", "没有在录音")
            return

        self.recording = False

        print("Finished recording.")
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.inference_button.config(state=tk.NORMAL)

        self.stream.stop_stream()
        self.stream.close()

        # Save the recorded data as a WAV file
        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))

    def perform_inference(self):
        try:
            input_wav = self.__read_audio_file__(self.output_filename)
            text = self.model_inference(input_wav, language="zh")
            self.temp_txt = text
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def searchAnswerFromZhipuAI(self):
        question = {
            "role": "user",
            "content": self.temp_txt
        }
        text = Remote_AI_Infer(question)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, text)

    def __read_audio_file__(self, input_filename, fs=16000, channels=1):
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
        return read_audio_file(input_filename)

    def __bind_events__(self):

        # 绑定键盘事件
        self.root.bind('<KeyPress-r>', self.start_recording)
        self.root.bind('<KeyPress-s>', self.stop_recording)

        # # 绑定鼠标事件
        # self.record_button.bind('<Button-1>', self.start_recording)
        # self.stop_button.bind('<Button-3>', self.stop_recording)

    def save_edit_text(self):
        self.temp_txt = self.output_text.get(1.0, tk.END).strip()
        # messagebox.showinfo("信息", "文本已保存")


if __name__ == "__main__":
    root = tk.Tk()
    # from AudioAPI import model_inference, read_audio_file

    app = AudioApp(root, model_inference)
    root.mainloop()
