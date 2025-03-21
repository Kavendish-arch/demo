# coding=utf-8

import os
import librosa
import base64
import io
import gradio as gr
import re

import numpy as np
import torch
import torchaudio

from funasr import AutoModel
from remoteDeepSeek.remote import remote_infer as Remote_AI_Infer

# 定义模型
model = "iic/SenseVoiceSmall"
model = AutoModel(model=model,
                  vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                  vad_kwargs={"max_single_segment_time": 30000},
                  trust_remote_code=True,
                  )

emo_dict = {
    "<|HAPPY|>": "😊",
    "<|SAD|>": "😔",
    "<|ANGRY|>": "😡",
    "<|NEUTRAL|>": "",
    "<|FEARFUL|>": "😰",
    "<|DISGUSTED|>": "🤢",
    "<|SURPRISED|>": "😮",
}

event_dict = {
    "<|BGM|>": "🎼",
    "<|Speech|>": "",
    "<|Applause|>": "👏",
    "<|Laughter|>": "😀",
    "<|Cry|>": "😭",
    "<|Sneeze|>": "🤧",
    "<|Breath|>": "",
    "<|Cough|>": "🤧",
}

emoji_dict = {
    "<|nospeech|><|Event_UNK|>": "❓",
    "<|zh|>": "",
    "<|en|>": "",
    "<|yue|>": "",
    "<|ja|>": "",
    "<|ko|>": "",
    "<|nospeech|>": "",
    "<|HAPPY|>": "😊",
    "<|SAD|>": "😔",
    "<|ANGRY|>": "😡",
    "<|NEUTRAL|>": "",
    "<|BGM|>": "🎼",
    "<|Speech|>": "",
    "<|Applause|>": "👏",
    "<|Laughter|>": "😀",
    "<|FEARFUL|>": "😰",
    "<|DISGUSTED|>": "🤢",
    "<|SURPRISED|>": "😮",
    "<|Cry|>": "😭",
    "<|EMO_UNKNOWN|>": "",
    "<|Sneeze|>": "🤧",
    "<|Breath|>": "",
    "<|Cough|>": "😷",
    "<|Sing|>": "",
    "<|Speech_Noise|>": "",
    "<|withitn|>": "",
    "<|woitn|>": "",
    "<|GBG|>": "",
    "<|Event_UNK|>": "",
}

lang_dict = {
    "<|zh|>": "<|lang|>",
    "<|en|>": "<|lang|>",
    "<|yue|>": "<|lang|>",
    "<|ja|>": "<|lang|>",
    "<|ko|>": "<|lang|>",
    "<|nospeech|>": "<|lang|>",
}

emo_set = {"😊", "😔", "😡", "😰", "🤢", "😮"}
event_set = {"🎼", "👏", "😀", "😭", "🤧", "😷", }


def format_str(s):
    for sptk in emoji_dict:
        s = s.replace(sptk, emoji_dict[sptk])
    return s


def format_str_v2(s):
    sptk_dict = {}
    for sptk in emoji_dict:
        sptk_dict[sptk] = s.count(sptk)
        s = s.replace(sptk, "")
    emo = "<|NEUTRAL|>"
    for e in emo_dict:
        if sptk_dict[e] > sptk_dict[emo]:
            emo = e
    for e in event_dict:
        if sptk_dict[e] > 0:
            s = event_dict[e] + s
    s = s + emo_dict[emo]

    for emoji in emo_set.union(event_set):
        s = s.replace(" " + emoji, emoji)
        s = s.replace(emoji + " ", emoji)
    return s.strip()


def format_str_v3(s):
    def get_emo(s):
        return s[-1] if s[-1] in emo_set else None

    def get_event(s):
        return s[0] if s[0] in event_set else None

    s = s.replace("<|nospeech|><|Event_UNK|>", "❓")
    for lang in lang_dict:
        s = s.replace(lang, "<|lang|>")
    s_list = [format_str_v2(s_i).strip(" ") for s_i in s.split("<|lang|>")]
    new_s = " " + s_list[0]
    cur_ent_event = get_event(new_s)
    for i in range(1, len(s_list)):
        if len(s_list[i]) == 0:
            continue
        if get_event(s_list[i]) == cur_ent_event and get_event(s_list[i]) != None:
            s_list[i] = s_list[i][1:]
        # else:
        cur_ent_event = get_event(s_list[i])
        if get_emo(s_list[i]) != None and get_emo(s_list[i]) == get_emo(new_s):
            new_s = new_s[:-1]
        new_s += s_list[i].strip().lstrip()
    new_s = new_s.replace("The.", " ")
    return new_s.strip()


# 模型推理
def model_inference(input_wav, language, fs=16000):
    """

    """
    # task_abbr = {"Speech Recognition": "ASR", "Rich Text Transcription": ("ASR", "AED", "SER")}
    language_abbr = {
        "auto": "auto", "zh": "zh", "en": "en", "yue": "yue", "ja": "ja", "ko": "ko",
        "nospeech": "nospeech"
    }

    # task = "Speech Recognition" if task is None else task
    language = "auto" if len(language) < 1 else language
    selected_language = language_abbr[language]
    # selected_task = task_abbr.get(task)

    # print(f"input_wav: {type(input_wav)}, {input_wav[1].shape}, {input_wav}")

    if isinstance(input_wav, tuple):
        fs, input_wav = input_wav
        input_wav = input_wav.astype(np.float32) / np.iinfo(np.int16).max
        if len(input_wav.shape) > 1:
            input_wav = input_wav.mean(-1)
        if fs != 16000:
            print(f"audio_fs: {fs}")
            resampler = torchaudio.transforms.Resample(fs, 16000)
            input_wav_t = torch.from_numpy(input_wav).to(torch.float32)
            input_wav = resampler(input_wav_t[None, :])[0, :].numpy()

    merge_vad = True  # False if selected_task == "ASR" else True

    print(f"language: {language}, merge_vad: {merge_vad}")
    text = model.generate(input=input_wav,
                          cache={},
                          language=language,
                          use_itn=True,
                          batch_size_s=60, merge_vad=merge_vad)

    print(text)
    text = text[0]["text"]
    text = format_str_v3(text)

    print(text)

    return text


audio_examples = [
    ["example/zh.mp3", "zh"],
    ["example/yue.mp3", "yue"],
    ["example/en.mp3", "en"],
    ["example/ja.mp3", "ja"],
    ["example/ko.mp3", "ko"],
    ["example/emo_1.wav", "auto"],
    ["example/emo_2.wav", "auto"],
    ["example/emo_3.wav", "auto"],
    # ["example/emo_4.wav", "auto"],
    # ["example/event_1.wav", "auto"],
    # ["example/event_2.wav", "auto"],
    # ["example/event_3.wav", "auto"],
    ["example/rich_1.wav", "auto"],
    ["example/rich_2.wav", "auto"],
    # ["example/rich_3.wav", "auto"],
    ["example/longwav_1.wav", "auto"],
    ["example/longwav_2.wav", "auto"],
    ["example/longwav_3.wav", "auto"],
    # ["example/longwav_4.wav", "auto"],
]

html_content = """
<div>
<h2 style="font-size: 22px;margin-left: 0px;">Voice Understanding Model: SenseVoice-Small</h2>
<p style="font-size: 18px;margin-left: 20px;">SenseVoice-Small is an encoder-only speech foundation model designed for rapid voice understanding. It encompasses a variety of features including automatic speech recognition (ASR), spoken language identification (LID), speech emotion recognition (SER), and acoustic event detection (AED). SenseVoice-Small supports multilingual recognition for Chinese, English, Cantonese, Japanese, and Korean. Additionally, it offers exceptionally low inference latency, performing 7 times faster than Whisper-small and 17 times faster than Whisper-large.</p>
<h2 style="font-size: 22px;margin-left: 0px;">Usage</h2> <p style="font-size: 18px;margin-left: 20px;">Upload an audio file or input through a microphone, then select the task and language. the audio is transcribed into corresponding text along with associated emotions (😊 happy, 😡 angry/exicting, 😔 sad) and types of sound events (😀 laughter, 🎼 music, 👏 applause, 🤧 cough&sneeze, 😭 cry). The event labels are placed in the front of the text and the emotion are in the back of the text.</p>
	<p style="font-size: 18px;margin-left: 20px;">Recommended audio input duration is below 30 seconds. For audio longer than 30 seconds, local deployment is recommended.</p>
	<h2 style="font-size: 22px;margin-left: 0px;">Repo</h2>
	<p style="font-size: 18px;margin-left: 20px;"><a href="https://github.com/FunAudioLLM/SenseVoice" target="_blank">SenseVoice</a>: multilingual speech understanding model</p>
	<p style="font-size: 18px;margin-left: 20px;"><a href="https://github.com/modelscope/FunASR" target="_blank">FunASR</a>: fundamental speech recognition toolkit</p>
	<p style="font-size: 18px;margin-left: 20px;"><a href="https://github.com/FunAudioLLM/CosyVoice" target="_blank">CosyVoice</a>: high-quality multilingual TTS model</p>
</div>
"""
html_content = ""

"""
这段代码使用了 **Gradio** 框架来构建一个交互式的Web界面。以下是主要的框架组件及其功能介绍：

1. **`gr.Blocks`**：  
   - 用于创建自定义布局的界面容器，支持灵活的行、列布局。
   - 在这里设置了主题为 `gr.themes.Soft()`，提供柔和的视觉风格。

2. **`gr.HTML`**：  
   - 用于在界面上嵌入自定义的HTML内容。
   - 在代码中，`html_content` 包含了模型的介绍、使用说明和相关链接。

3. **`gr.Row` 和 `gr.Column`**：  
   - 用于定义布局结构。
   - `gr.Row` 表示水平排列的组件，`gr.Column` 表示垂直排列的组件。
   - 在代码中，音频输入框、语言选择下拉框、启动按钮和结果输出框被放置在一个列布局中。

4. **`gr.Audio`**：  
   - 用于上传音频文件或通过麦克风录制音频。
   - 标签为 "Upload audio or use the microphone"。

5. **`gr.Dropdown`**：  
   - 用于创建下拉选择框。
   - 提供了语言选项，包括自动检测（`auto`）、中文（`zh`）、英文（`en`）、粤语（`yue`）、日语（`ja`）、韩语（`ko`）和无语音（`nospeech`）。

6. **`gr.Button`**：  
   - 用于创建按钮。
   - 标签为 "Start"，点击后会触发指定的回调函数。

7. **`gr.Textbox`**：  
   - 用于显示文本输出。
   - 标签为 "Results"，用于展示推理结果。

8. **`gr.Examples`**：  
   - 用于展示预定义的示例数据。
   - 用户可以通过这些示例快速测试模型的功能。

9. **`fn_button.click`**：  
   - 绑定按钮点击事件。
   - 当用户点击 "Start" 按钮时，调用 `model_inference` 函数进行推理，并将结果显示在 `text_outputs` 中。

# 控制流图
```mermaid
flowchart TD
    A[初始化界面] --> B[添加HTML内容]
    B --> C[创建音频输入组件]
    C --> D[创建语言选择下拉框]
    D --> E[创建启动按钮和结果输出框]
    E --> F[绑定按钮点击事件]
    F --> G[启动Web应用]
```

"""


def launch():
    """
启动一个图形用户界面(GUI)应用，用于上传音频、选择语言并启动处理以获取结果。
该函数定义了GUI的布局和组件，以及用户交互的回调函数。
"""
    # 创建一个带有Soft主题的Blocks对象作为GUI的基础结构
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        # 显示Markdown格式的描述信息（已注释掉，不显示描述）
        # gr.Markdown(description)

        # 显示HTML内容
        gr.HTML(html_content)
        # 创建一个行容器，用于布局管理
        with gr.Row():
            # 创建一个列容器，用于布局管理
            with gr.Column():
                # 添加一个音频输入组件，允许用户上传音频或使用麦克风录音
                audio_inputs = gr.Audio(label="Upload audio or use the microphone")
                # 创建一个配置区域，可以展开/折叠
                with gr.Accordion("Configuration"):
                    # 添加一个下拉菜单，用于选择语言
                    language_inputs = gr.Dropdown(
                        choices=["auto", "zh", "en", "yue", "ja", "ko", "nospeech"],
                        value="auto",
                        label="Language")
                    # 添加一个主要按钮，用于启动音频处理
                    fn_button = gr.Button("Start", variant="primary")
                    # 添加一个主要按钮，用于启动文字推理
                    fn_button_infer = gr.Button("AI Infer", variant="secondary")

                    # 添加一个文本输出框，用于显示处理结果
                    text_outputs = gr.Textbox(label="Results")

                    # 添加一个文本输出框，用于显示推理结果
                    text_answer_outputs = gr.Textbox(label="质谱清言回答")

        # 定义按钮点击事件的回调函数，执行模型推理，并将结果输出到文本框中
        fn_button.click(model_inference, inputs=[audio_inputs, language_inputs], outputs=text_outputs)

        fn_button_infer.click(Remote_AI_Infer, inputs=[text_outputs, language_inputs], outputs=text_answer_outputs)
        # 	# 添加示例音频，以供用户参考
        # gr.Examples(examples=audio_examples, inputs=[audio_inputs, language_inputs], examples_per_page=20)

        # 启动GUI应用
        demo.launch()


if __name__ == "__main__":
    # iface.launch()
    launch()
