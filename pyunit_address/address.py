#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from .multitree import MultiTree, singleton, remove_subset
from collections.abc import Iterable
import ahocorasick
import bz2
import os
import json
import re
import itertools


@singleton
class Address:

    def __init__(self, is_max_address=False):
        """初始化

        :param is_max_address: 满足最长地址
        """

        # 加载精准匹配的词库，共40万
        self.suffix_stop = '[省市县区]'
        self.ac = ahocorasick.Automaton()
        self.count = itertools.count(0)
        self.is_max_address = is_max_address
        self.root = self._unzip()

    def delete_vague_text(self, words: [str, Iterable]):
        """删除默认词库

        传入的参数可以是：一个词语、一个列表、一个元组、甚至是一个文件地址，文件地址里面是包含一列一个词语

        格式1：删除一个词，传入字符串

        格式2：删除一列词，传入列表
        """
        if isinstance(words, str):
            if os.path.exists(words):
                with open(words, encoding='UTF-8')as fp:
                    for word in fp:
                        self.ac.remove_word(word)
            else:
                self.ac.remove_word(words)
        elif isinstance(words, Iterable):
            for word in words:
                self.ac.remove_word(word)

    def add_vague_text(self, words: [str, Iterable], separators='-'):
        """增加地址词语

        传入的参数可以是：一个词语、一个列表、一个元组、甚至是一个文件地址，文件地址里面是包含一列一个词语

        格式1： 只增加一个词

        格式2：增加一个列表

        :param words: 可以传列表、文件地址、或者字符串，如果字符串包含separators，则默认为传入有序地址，
                      比如：贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台
                      传入有序地址后，可以进行补全地址。
                      如果单独传入一个字符串，只能找到该字符串不能进行补全地址。

        :param separators: 地址分割符，比如：贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台、分割符是：-
        """
        if isinstance(words, str):
            if os.path.exists(words):  # 判断是否存在该文件
                with open(words, encoding='UTF-8')as fp:
                    for word in fp:
                        self.add_vague_text(word, separators)
            elif separators in words:  # 判断是否带有分割符
                ls = words.split(separators)
                for key in ls:
                    self.flag_ac_contain_key(key)
                self.root.add_value(words, separators)
            else:  # 纯字符串
                self.flag_ac_contain_key(words)
        elif isinstance(words, Iterable):  # 迭代器
            for word in words:
                self.add_vague_text(word, separators)

    def flag_ac_contain_key(self, key):
        """判断ac自动机里面是否包含相同的key值"""
        if key not in self.ac:
            stop_key = re.sub(self.suffix_stop, '', key)
            flag = True if len(stop_key) <= 1 else (stop_key == key)
            flag or self.ac.add_word(stop_key, [key, next(self.count)])
            self.ac.add_word(key, [key, next(self.count)])

    def _unzip(self) -> (list, dict):
        """解压地址数据包"""
        name = 'address'
        bz = bz2.BZ2File(os.path.dirname(__file__) + os.sep + name + '.bz2')
        lines = bz.read().decode('utf-8')
        address = json.loads(lines[512:-1134], encoding='utf8')
        root = MultiTree(value='中国', parent=None)
        for one_k, one_v in address.items():
            self.flag_ac_contain_key(one_k)
            one = MultiTree(value=one_k, parent=root)
            root.add_children(one)
            for two_k, two_v in one_v.items():
                self.flag_ac_contain_key(two_k)
                two = MultiTree(value=two_k, parent=one)
                one.add_children(two)
                for three_k, three_v in two_v.items():
                    self.flag_ac_contain_key(three_k)
                    three = MultiTree(value=three_k, parent=two)
                    two.add_children(three)
                    for four_k, four_v in three_v.items():
                        four_k = self.reset_key(four_k)
                        self.flag_ac_contain_key(four_k)
                        four = MultiTree(value=four_k, parent=three)
                        three.add_children(four)
                        for five_k in four_v:
                            five_k = self.reset_key(five_k)
                            self.flag_ac_contain_key(five_k)
                            five = MultiTree(value=five_k, parent=four)
                            four.add_children(five)
        return root

    def find_address(self, data: str, is_max_address=True, ignore_special_characters=True) -> list:
        """查找地址

        :param data: 查找地址数据
        :param is_max_address: 是否查找最长地址
        :param ignore_special_characters: 是否去掉特殊字符
        :return: 地址列表
        """
        if ignore_special_characters:
            data = re.sub(r"[!#$%&'()*+,-./:：，。？！；‘’、《》;<=>?@[\]^_`{|}~\s]", '', data)
        ls = self.max_match_cut(data)
        if is_max_address:
            max_address = []
            match = re.sub('|'.join(ls), lambda x: '*' * len(x.group()), data)
            for addr in re.finditer(r'[*]+', match):
                max_address.append(data[addr.start():addr.end()])
            return max_address
        return ls

    def supplement_address(self, address_name, is_max_address=None, is_order=False, link: str = '-') -> list:
        """补全地址

        输入零碎的地址信息。补全地址，比如输入：山西孝义,补全为：山西省-吕梁市-文水县-孝义镇

        当参数：is_max_address=False时。默认补全最短地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_max_address=True。补全最长地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇-孝义村委会

        当参数：is_order=False。补全的地址是无序的，比如：孝义山西，也能补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_order=True。补全的地址是有序的，比如：孝义山西，则补全不出。无法在孝义下面找到关于山西的地址字眼。

        :param address_name: 要补全的地址，比如：山西孝义
        :param is_max_address: 是否是最大补全地址，默认是否。
        :param is_order: 地址补全，是否遵守顺序。默认是：无序
        :param link: 补全路径的拼接符，默认是：-
        """
        ls = []
        keys = self.max_match_cut(address_name)
        for key in keys:
            prototype = self.ac.get(key)[0]
            address = self.root.search(prototype, link)
            ls.extend(address)
        match = list(filter(self.satisfy_filter(keys, is_order), ls))
        ls = remove_subset(match)
        if is_max_address is True:
            return [max(ls, key=lambda x: len(x))]
        elif is_max_address is False:
            return [min(ls, key=lambda x: len(x))]
        return ls

    @staticmethod
    def satisfy_filter(finds_address, is_order):
        """满足条件的过滤算法

        保证每一个key都在地址中

        算法流程：满足每一个地址提取的实体
        """

        def _(x):
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

        return _

    def max_match_cut(self, sentence):
        """正向最长匹配算法"""
        words = ['']
        for i in sentence:
            if self.ac.match(words[-1] + i):
                words[-1] += i
            else:
                words.append(i)
        values = list(filter(lambda x: len(x) > 1, words))
        return [v for v in values if v in self.ac]  # 检验是否在ac自动机里面的词语

    @staticmethod
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
