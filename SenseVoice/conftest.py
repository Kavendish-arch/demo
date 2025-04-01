#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：conftest.py
@Author  ：chenyingtao
@Date    ：2025/3/27 17:58 
"""
import pytest


@pytest.fixture(scope="function", autouse=True)
# 默认所有函数自动调用
def exe_mysql():
    print("连接数据库")
    yield
    print("关闭数据库")

@pytest.fixture(scope="module", autouse=True)
def exe_redis():
    print("连接redis")
    yield
    print("关闭redis")