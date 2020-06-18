#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/6 12:36
# @Author: Jtyoui@qq.com
# @interpret: 自动补全地址
from collections.abc import Iterable

from .tool import remove_subset


def satisfy_filter(finds_address, is_order):
    """满足条件的过滤算法

    保证每一个key都在地址中

    算法流程：满足每一个地址提取的实体
    """

    def inner(x):
        order = []
        for address in finds_address:
            if address not in x:
                return False
            else:
                order.append(x.find(address))
        else:
            if is_order:
                return True if order == list(sorted(order)) else False
            return True

    return inner


def search(cls, link: str = '-') -> str:
    """搜索该值的路径

    :param cls: 多叉树对象
    :param link: 拼接符
    :return: 该值的路径
    """
    n = []
    while cls.parent:
        n.append(cls.value)
        cls = cls.parent
    return link.join(reversed(n))


def key_to_address(cls, keys):
    """根据关键字获取地址

    :param cls: Address类对象
    :param keys: 关键字
    :return: 返回关键字对应的地址
    """
    all_ = []
    if isinstance(keys, str):
        objs = cls.ac.get(keys)
        address = [search(obj) for obj in objs]
        return address
    elif isinstance(keys, Iterable):
        for key in keys:
            objs = cls.ac.get(key)
            address = [search(obj) for obj in objs]
            all_.extend(address)
    return all_


def supplement_address(cls, address_name, is_max_address=None, is_order=False, link: str = '-') -> list:
    """补全地址

    输入零碎的地址信息。补全地址，比如输入：山西孝义,补全为：山西省-吕梁市-文水县-孝义镇

    当参数：is_max_address=False时。默认补全最短地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇
    当参数：is_max_address=True。补全最长地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇-孝义村委会

    当参数：is_order=False。补全的地址是无序的，比如：孝义山西，也能补全为：山西省-吕梁市-文水县-孝义镇
    当参数：is_order=True。补全的地址是有序的，比如：孝义山西，则补全不出。无法在孝义下面找到关于山西的地址字眼。

    :param cls: Address类对象
    :param address_name: 要补全的地址，比如：山西孝义
    :param is_max_address: 是否是最大补全地址，默认是否。
    :param is_order: 地址补全，是否遵守顺序。默认是：无序
    :param link: 补全路径的拼接符，默认是：-
    """
    keys = cls.max_match_cut(address_name)
    all_ = key_to_address(cls, keys)
    match = filter(satisfy_filter(keys, is_order), all_)  # 根据过滤算法来去掉不是关键字的地址
    ls = remove_subset(match)
    if ls:
        if is_max_address is True:
            return [max(ls, key=lambda x: len(x))]
        elif is_max_address is False:
            return [min(ls, key=lambda x: len(x))]
    return ls
