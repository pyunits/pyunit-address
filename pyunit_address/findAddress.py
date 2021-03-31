#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/6 12:31
# @Author: Jtyoui@qq.com
# @interpret: 自动寻找地址
import re
from .tool import remove_subset


def checkout_re_address(address, text):
    """检验是否是有效地址
    检验： xx省xx市xx组团x栋|xx（号）楼xx层|x座
    xx的有效数字不超过5位数
    """
    compiles = re.search(rf'{address}(\w+?)([a-zA-Z\d]+组团|[栋楼层座])', text, flags=re.S)
    if compiles:
        addr = compiles.group(1)
        if '的' not in addr:
            return compiles.group()
    else:
        compiles = re.search(rf'{address}(\w+?)\d+号', text, flags=re.S)
        return compiles.group() if compiles else False
    return False


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
            address = data[addr.start():addr.end()]
            address = checkout_re_address(address, data)
            if address:
                max_address.append(address)
        return remove_subset(max_address) if max_address else []
    return ls
