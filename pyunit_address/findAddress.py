#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/6 12:31
# @Author: Jtyoui@qq.com
# @interpret: 自动寻找地址
import re


def find_address(cls, data: str, is_max_address=True, ignore_special_characters=True) -> list:
    """查找地址

    :param cls: Address类对象
    :param data: 查找地址数据
    :param is_max_address: 是否查找最长地址
    :param ignore_special_characters: 是否去掉特殊字符
    :return: 地址列表
    """
    if ignore_special_characters:
        data = re.sub(r"[!#$%&'()*+,-./:：，。？！；‘’、《》;<=>?@[\]^_`{|}~\s]", '', data)
    ls = cls.max_match_cut(data)
    if is_max_address:
        max_address = []
        match = re.sub('|'.join(sorted(ls, key=lambda x: len(x), reverse=True)), lambda x: '*' * len(x.group()), data)
        for addr in re.finditer(r'[*]+', match):
            max_address.append(data[addr.start():addr.end()])
        return max_address
    return ls
