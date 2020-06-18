#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/6 12:39
# @Author: Jtyoui@qq.com
# @interpret: 自动纠错地址
"""这里的纠错是表示地址错误，并不是说文字错误，比如：四川省，写成：四穿省，并不会纠错。
例如：正确的地址：贵州省贵阳市花溪区
     错误的地址：贵州省遵义市花溪区

会自动纠正为：贵州省贵阳市花溪区
"""
from .supplementAddress import key_to_address


def max_key_filter(keys):
    """最多关键词过滤算法

    依据关键词出现的次数来判断改地址的重要性
    """

    def inner(x):
        flag = 0
        for key in keys:
            if key in x:
                flag += 1
        return flag

    return inner


def correct_address(cls, sentence):
    """自动纠错地址

    :param cls: Address类对象
    :param sentence: 要纠错的句子
    :return: 纠错后的地址
    """
    keys = cls.max_match_cut(sentence)
    all_ = key_to_address(cls, keys)
    filter_address = list(sorted(all_, key=max_key_filter(keys), reverse=True))
    if filter_address:
        max_address = max(filter_address, key=lambda x: len(x))
        return max_address
    return filter_address
