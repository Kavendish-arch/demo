# coding=utf-8


import gradio as gr

import numpy as np
import torch
import torchaudio

from funasr import AutoModel
from paddleocr import PaddleOCR

from remoteDeepSeek.remote import remote_infer as Remote_AI_Infer

def model_inference_image(img_path, language_inputs:str="ch"):
        """

        通过调用PaddleOCR引擎实现对给定图片的光学字符识别（OCR）。
        Args:
            img: Image for OCR. It can be an ndarray, img_path, or a list of ndarrays.
        返回:
        str: 识别到的文本内容，每行文本末尾包含换行符。
        """
        # 初始化PaddleOCR引擎，包含角度分类，语言设置为中文。
        # 该初始化过程只需执行一次，以下载并加载模型到内存中。
        ocr = PaddleOCR(use_angle_cls=True, lang=language_inputs)

        # 执行OCR识别，包含角度分类。
        result = ocr.ocr(img_path, cls=True)

        # 初始化一个空字符串，用于存储所有识别到的文本。
        txt = ""
        # 遍历识别结果的每一项。
        for idx in range(len(result)):
            res = result[idx]
            # 遍历每一项中的每一行文本。
            for line in res:
                # 将识别到的文本添加到结果字符串中，每行文本末尾添加换行符。
                txt += line[1][0] + "\n"
        # 返回识别到的全部文本。
        return txt

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

html_content = """"""


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
                with gr.Accordion("输入区域"):

                    # 添加一个音频输入组件，允许用户上传音频或使用麦克风录音
                    audio_inputs = gr.Audio(label="Upload audio or use the microphone")

                    # 增加一个图片输入组件，允许用户上传图片
                    image_inputs = gr.Image(label="Upload image")

                # 创建一个配置区域，可以展开/折叠
                with gr.Accordion("配置"):
                    # 添加一个下拉菜单，用于选择语言
                    language_inputs = gr.Dropdown(
                        choices=["auto", "zh", "en", "yue", "ja", "ko", "nospeech"],
                        value="auto",
                        label="Language")
                    # 添加一个主要按钮，用于启动音频处理
                    fn_Button_A2T = gr.Button("语音转文字", variant="primary")
                    fn_Button_OCR = gr.Button("Image OCR", variant="secondary")

                    # 添加一个主要按钮，用于启动文字推理
                    fn_button_infer = gr.Button("AI Infer", variant="secondary")

                    # 添加一个文本输出框，用于显示处理结果
                    text_outputs = gr.Textbox(label="Results")

                    # 添加一个文本输出框，用于显示推理结果
                    text_answer_outputs = gr.Textbox(label="质谱清言回答")

        # 定义按钮点击事件的回调函数，执行模型推理，并将结果输出到文本框中
        fn_Button_A2T.click(model_inference, inputs=[audio_inputs, language_inputs], outputs=text_outputs)
        # OCR 功能开始按钮

        fn_Button_OCR.click(model_inference_image, inputs=[image_inputs], outputs=text_outputs)
        # 大模型回答问题功能
        fn_button_infer.click(Remote_AI_Infer, inputs=[text_outputs, language_inputs], outputs=text_answer_outputs)

        # 启动GUI应用
        demo.launch()


if __name__ == "__main__":

    launch()
