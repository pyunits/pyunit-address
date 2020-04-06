#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from pyunit_address import *
import time

address = Address(is_max_address=True)
address.add_vague_text(['红花岗', '花溪'])
address.add_vague_text('贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台')


def test():
    af = find_address(address, '我家在贵州遵义红花岗区，你家在贵州贵阳花溪区')
    print(af)  # ['贵州遵义红花岗区', '贵州贵阳花溪区']


def test_add():
    af = find_address(address, '我家在贵州遵义红花岗区，你家在贵州贵阳花溪')
    print(af)  # ['贵州遵义红花岗区', '贵州贵阳花溪']


def test_delete():
    af = find_address(address, '贵州省贵阳市花溪区瑞华社区服务中心万科，你家在贵州贵阳花溪区')
    print(af)  # ['贵州省贵阳市花溪区瑞华社区', '贵州贵阳花溪区']


def test_supplement_address():
    print(supplement_address(address, '我家在遵义市乐石台', is_order=True))  # ['贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台']
    print(supplement_address(address, '山西孝义镇'))  # ['山西省-吕梁市-文水县-孝义镇']
    print(supplement_address(address, '我在三家镇乐安村'))  # ['海南省-省直辖县级行政区划-东方市-三家镇-乐安村']
    print(supplement_address(address, '我在新舟镇'))  # ['贵州省-遵义市-遵义县-新舟镇']


if __name__ == '__main__':
    start = time.time()
    test()
    test_add()
    test_delete()
    test_supplement_address()
    print(time.time() - start)
