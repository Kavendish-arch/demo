#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：testAudioAPI.py
@Author  ：chenyingtao
@Date    ：2025/3/27 16:58 
"""



### 1. `model_inference` 函数
"""
"""
# **测试点：**
# - **正常情况：**
#   - 输入有效的音频数据和语言参数。
#   - 输入不同语言参数（如 "zh", "en"）。
# - **边界情况：**
#   - 输入空字符串或无效语言参数。
#   - 输入的音频采样率与默认值不同。
#   - 输入的音频数据为单声道和立体声。
# - **异常情况：**
#   - 输入的音频数据格式不正确。
#   - 输入的音频数据为空。

def test_model_inference():
    assert model_inference((16000, np.random.rand(16000)), "zh") == "你好，我是一个语音识别模型。"
    assert model_inference((8000, np.random.rand(8000)), "en") == "Hello, I am a voice recognition model."
    assert model_inference((16000, np.random.rand(16000)), "") == "你好，我是一个语音识别模型。"

# **示例测试用例：**
# - `model_inference((16000, np.random.rand(16000)), "zh")`
# - `model_inference((8000, np.random.rand(8000)), "en")`
# - `model_inference((16000, np.random.rand(16000)), "")`
# - `model_inference((16000, np.random.rand(16000)), "invalid_language")`
# - `model_inference((16000, np.array([], dtype=np.int16)), "zh")`

### 2. `read_audio_file` 函数

# **测试点：**
# - **正常情况：**
#   - 输入有效的单声道和立体声音频文件。
#   - 输入不同采样率的音频文件。
# - **边界情况：**
#   - 输入的音频文件采样率与默认值不同。
#   - 输入的音频文件通道数与默认值不同。
# - **异常情况：**
#   - 输入不存在的音频文件路径。
#   - 输入的音频文件格式不正确。
#   - 输入的音频文件为空。
#
# **示例测试用例：**
# - `read_audio_file("audioWs/output.wav")`
# - `read_audio_file("audioWs/output_stereo.wav")`
# - `read_audio_file("audioWs/output_8k.wav")`
# - `read_audio_file("nonexistent_file.wav")`
# - `read_audio_file("audioWs/invalid_format.txt")`
#
# ### 3. `remove_bracketed_text` 函数
#
# **测试点：**
# - **正常情况：**
#   - 输入包含尖括号及其内容的字符串。
#   - 输入不包含尖括号及其内容的字符串。
# - **边界情况：**
#   - 输入空字符串。
#   - 输入仅包含尖括号及其内容的字符串。
# - **异常情况：**
#   - 输入非字符串类型的数据。
#
# **示例测试用例：**
# - `remove_bracketed_text("这是一个<|示例|>文本")`
# - `remove_bracketed_text("这是一个示例文本")`
# - `remove_bracketed_text("")`
# - `remove_bracketed_text("<|尖括号|>")`
# - `remove_bracketed_text(12345)`

### 总结
