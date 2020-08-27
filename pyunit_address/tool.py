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


def flask_content_type(requests):
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if 'application/x-www-form-urlencoded' == requests.content_type:
            data = requests.form
        else:  # 无法被解析出来的数据
            raise Exception('POST的Content-Type必须是:application/x-www-form-urlencoded')
    elif requests.method == 'GET':
        data = requests.args
    else:
        raise Exception('只支持GET和POST请求')
    data = dict(data)
    is_max_address = data.get('is_max_address', None)
    if is_max_address and is_max_address.lower() == 'false':
        data['is_max_address'] = False
    is_order = data.get('is_order', None)
    if is_order and is_order.lower() == 'false':
        data['is_order'] = False
    ignore_special_characters = data.get('ignore_special_characters', None)
    if ignore_special_characters and ignore_special_characters.lower() == 'false':
        data['ignore_special_characters'] = False
    return data
