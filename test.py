#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from pyunit_address import Address


def test():
    address = Address(is_max_address=True)
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪区')
    print(af)


def test_add():
    address = Address(is_max_address=True)
    address.add_vague_text('红花岗')  # 在默认词库上追加地址词库
    address.add_vague_text('花溪')
    # address.add_vague_text(['红花岗', '花溪'])
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪')
    print(af)


def test_load():
    address = Address(is_max_address=True)
    address.set_vague_text(['红花岗', '花溪'])  # 加载词库，替换默认词库
    # address.set_vague_text('自定义词库.txt')
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪')
    print(af)


def test_delete():
    address = Address(is_max_address=True)
    af = address.find_address('贵州省贵阳市花溪区瑞华社区服务中心万科居委会珠江路368号25栋10层1006号，你家在贵州贵阳花溪区')
    print(af)


def test_supplement_address():
    address = Address(is_max_address=True)
    asu = address.supplement_address('我家在贵州贵阳观山湖')  # ['贵州省-贵阳市-观山湖区']
    print(asu)


def test_remove():
    address = Address(is_max_address=True)
    r = address.remove_subset(['a', 'a', 'ab'])
    print(r)


if __name__ == '__main__':
    # test()
    # test_add()
    # test_load()
    # test_delete()
    test_supplement_address()
    # test_remove()
