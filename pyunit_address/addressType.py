# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/8/27 上午10:32
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : 获取地址的类型
import os
import time
import zipfile

from .address import Address
from .correctionAddress import correct_address
from .findAddress import find_address
from .supplementAddress import supplement_address


class AddressType:

    def __init__(self):
        self.hot = {}
        # 加载文本初始化
        hot_file = os.environ.get('PYUNIT_ADDRESS_HOT_FILE', None)
        if hot_file:
            with open(hot_file, encoding='utf-8') as fp:
                for line in fp.readlines():
                    name, addr = line.strip().split()
                    self.hot[name] = addr
        else:
            zip_file = os.path.join(os.path.dirname(__file__), 'hot.zip')
            zips = zipfile.ZipFile(zip_file, 'r')
            data = zips.read('hot.txt').decode('utf-8')
            for line in data.split('\r\n'):
                if line:
                    name, addr = line.replace(' ', '').split('\t')
                    self.hot[name] = addr
        self.address = Address()

    @staticmethod
    def get_address_type(address):
        """根据地址信息来细化类型

        类型包括:
            中国省份
            中国城市
            中国城市区县
            中国城市街道
            中国地理热点

        >>> AddressType().get_address_type('云南省')
        '省份'

        >>> AddressType().get_address_type('贵州省贵阳市')
        '城市'

        >>> AddressType().get_address_type('金阳路105号')
        '街道'

        >>> AddressType().get_address_type('观山湖区')
        '区县'

        :param address: 输入一个地址文本
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

    def address_message(self, word):
        """根据一个地址文本，分析出改文本中的地址和景点地区"""
        start = time.time()
        result = []
        for key in self.hot:
            if word and key in word:
                types = '地理热点'
                ca = self.hot[key]
                result.append({'address': key, 'supplement_address': [], 'correct_address': ca, 'type': types})
        finds = find_address(self.address, word)
        for find in finds:
            sa = supplement_address(self.address, find)  # 补全地址
            ca = correct_address(self.address, find)  # 纠错地址
            s = [{'key': i} for i in sa]
            types = self.get_address_type(ca)
            result.append({'address': find, 'supplement_address': s, 'correct_address': ca, 'type': types})
        print(time.time() - start)
        return result

    def add_vague_text(self, words, separators):
        self.address.add_vague_text(words, separators)

    def delete_vague_text(self, words):
        self.address.delete_vague_text(words)
