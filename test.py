#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
import time

from pyunit_address import *

address = Address(is_max_address=True)
address.add_vague_text(['红花岗', '花溪'])
address.add_vague_text('贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台')


def find_address_test():
    af = find_address(address, '我家在贵州遵义红花岗区，你家在贵州贵阳花溪区')
    print(af)  # ['贵州遵义红花岗区', '贵州贵阳花溪区']


def test_supplement_address():
    print(supplement_address(address, '我家在遵义市乐石台', is_order=True))  # ['贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台']
    print(supplement_address(address, '山西孝义镇'))  # ['山西省-吕梁市-文水县-孝义镇']
    print(supplement_address(address, '我在三家镇乐安村'))  # ['海南省-省直辖县级行政区划-东方市-三家镇-乐安村']
    print(supplement_address(address, '我在新舟镇'))  # ['贵州省-遵义市-遵义县-新舟镇']


def correct_address_test():
    print(correct_address(address, '贵州省遵义市花溪区', False))  # ['贵州省-遵义市', '贵州省-贵阳市-花溪区'],未开启最长地址


def all_test():
    string_ = '我家在红花岗，你家在贵州贵阳花溪区,他家在贵州省遵义市花溪区'
    finds = find_address(address, string_)
    for find in finds:
        print()
        print('地址', find)
        print('补全地址', supplement_address(address, find))
        print('纠错地址', correct_address(address, find))
        print('--------------------------')


if __name__ == '__main__':
    start = time.time()
    find_address_test()
    test_supplement_address()
    correct_address_test()
    all_test()
    print(time.time() - start)
