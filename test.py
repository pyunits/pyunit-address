#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from pyunit_address import Address


def test():
    address = Address(is_max_address=True)
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪区')
    print(af)  # ['贵州遵义红花岗区', '贵州贵阳花溪区']


def test_add():
    address = Address(is_max_address=True)
    address.add_vague_text(['红花岗', '花溪'])
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪')
    print(af)  # ['贵州遵义红花岗区', '贵州贵阳花溪']


def test_delete():
    address = Address(is_max_address=True)
    af = address.find_address('贵州省贵阳市花溪区瑞华社区服务中心万科，你家在贵州贵阳花溪区')
    print(af)  # ['贵州省贵阳市花溪区瑞华社区', '贵州贵阳花溪区']


def test_supplement_address():
    address = Address()
    address.add_vague_text('贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台')
    print(address.supplement_address('我家在遵义市乐石台', is_order=True))  # ['贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台']
    print(address.supplement_address('山西孝义'))  # ['山西省-吕梁市-文水县-孝义镇']
    print(address.supplement_address('我在乐安村'))  # ['贵州省-贵阳市-花溪区']


if __name__ == '__main__':
    test()
    test_add()
    test_delete()
    test_supplement_address()
