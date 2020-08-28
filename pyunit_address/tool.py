#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/6 12:29
# @Author: Jtyoui@qq.com
# @interpret： 常用工具
def remove_subset(ls) -> list:
    """去除列表中的子集

    比如：['aa','a','ab'] --> ['aa','ab']

    :param ls: 字符串列表
    :return: 返回去重后的结果
    """
    ls = sorted(ls, key=lambda x: len(x), reverse=True)
    total = []
    for subset in ls:
        if subset not in total:
            flag = True
            for word in total:
                if subset in word:
                    flag = False
                    break
            if flag:
                total.append(subset)
    return total


def reset_key(key):
    """重新设置key

    比如：有一些地名是： xx街道办事处 -> xx街道
                       xx村委会 -> xx村
                       等等
    """
    if key.endswith('社区居委会'):
        key = key[:-3]
    elif key.endswith('村委会'):
        key = key[:-2]
    elif key.endswith('街道办事处'):
        key = key[:-3]
    elif key.endswith('村村民委员会'):
        key = key[:-5]
    elif key == '居委会':
        key = '\x02'
    return key
