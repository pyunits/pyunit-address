# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/8/27 上午10:32
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : 获取地址的类型

def get_address_type(address):
    """根据地址信息来细化类型

    类型包括:
        中国省份
        中国城市
        中国城市区县
        中国城市街道
        中国地理热点

    >>> get_address_type('云南省')
    省份

    >>> get_address_type('贵州省贵阳市')
    城市

    >>> get_address_type('金阳路105号')
    街道

    >>> get_address_type('观山湖区')
    区县

    :param address: 输入一个地址
    :return: 地址类型
    """
    if '区' in address or '县' in address:
        return '区县'
    elif '路' in address or '号' in address:
        return '街道'
    elif '市' in address:
        return '城市'
    elif '省' in address:
        return '省份'
    return None
