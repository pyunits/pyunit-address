#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/6 12:39
# @Author: Jtyoui@qq.com
# @interpret: 自动纠正地址
"""这里的纠正是表示地址错误，并不是说文字错误，比如：四川省，写成：四穿省，并不会纠错。
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
        return x, flag

    return inner


def correct_address(cls, sentence, max_length_address=True):
    """自动纠正地址

    :param cls: Address类对象
    :param sentence: 要纠错的句子
    :param max_length_address: 是否返回最长地址
    :return: 纠错后的地址
    """
    max_seq_list = []
    keys = cls.max_match_cut(sentence)  # 分割地址关键词
    all_ = key_to_address(cls, keys)  # 根据关键词搜索地址
    filter_address = dict(map(max_key_filter(keys), all_))  # 判断关键词出现的频率
    if filter_address:
        sort_address = list(sorted(filter_address.items(), key=lambda x: x[1], reverse=True))  # 根据频率排序
        max_seq = sort_address[0][1]  # 获取最大的频率
        for address, flag in sort_address:
            if max_seq == flag:
                max_seq_list.append(address)  # 获取最大的频率组
        if max_length_address:
            return max(max_seq_list, key=lambda x: len(x))  # 返回字符串最长的一个地址
        else:
            return max_seq_list
    return []
