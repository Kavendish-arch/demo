#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：main.py
@Author  ：chenyingtao
@Date    ：2025/3/19 18:09 
"""

import tkinter as tk
from Audio2Txt.gui import AudioApp

if __name__ == "__main__":
    root = tk.Tk()
    from AudioAPI import model_inference, read_audio_file

    app = AudioApp(root, model_inference)
    root.mainloop()
