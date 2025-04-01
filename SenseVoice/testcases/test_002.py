#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：test_002.py
@Author  ：chenyingtao
@Date    ：2025/3/27 16:58 
"""
import allure
import pytest
from conftest import *

@pytest.mark.run(order=2)
# 函数形式运行
def test_login():
    print("test_login")


@pytest.mark.run(order=1)
def test_login2():
    print("test_login1")


@pytest.mark.skipif(2 < 3, reason="条件成立 跳过")
def test_logout():
    print("test_logout")


# 方法形式运行
class TestLogin:

    @pytest.mark.skip(reason="方法用例 跳过")
    def test_login(self):
        print("test_login")


@pytest.mark.xfail(reason="预期失败")
def test_login3():
    # 1 / 0
    print("test_login3")

def get_csv_data():
    import csv
    lists = []
    with open("./data/data.csv", "r", encoding="utf-8") as f:
        data = csv.reader(f)
        for row in data:
            lists.append(row)

        return lists


# @pytest.mark.parametrize(["username", "password"], [("admin", "123456"),
#                                                     ("admin", "1111"),
#                                                     ("adssmin", "1111s11")])
@pytest.mark.parametrize("username, password, assert_msg", get_csv_data())
@allure.severity(allure.severity_level.CRITICAL)
@allure.step(title="登录模块")
def test_login4(username, password, assert_msg):
    print("现在去登录")
    print("输入用户名", username)
    print("输入密码", password)

    allure.attach("描述", "")
