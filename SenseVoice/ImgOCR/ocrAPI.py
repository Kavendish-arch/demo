#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：ocrAPI.py
@Author  ：chenyingtao
@Date    ：2025/3/22 17:12 
"""
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr supports Chinese, English, French, German, Korean and Japanese
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order


def model_inference_image(img_path, language_inputs: str = "ch"):

    """

    通过调用PaddleOCR引擎实现对给定图片的光学字符识别（OCR）。

    Args:
        img: Image for OCR. It can be an ndarray, img_path, or a list of ndarrays.
    返回:
    str: 识别到的文本内容，每行文本末尾包含换行符。
    """
    # 初始化PaddleOCR引擎，包含角度分类，语言设置为中文。
    # 该初始化过程只需执行一次，以下载并加载模型到内存中。
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')

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


if __name__ == '__main__':
    img_path = '../img/6edf61a4f1353e4472a7317f2bafe88.jpg'
    print( model_inference_image(img_path))