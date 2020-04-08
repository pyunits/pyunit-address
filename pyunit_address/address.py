#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
# @interpret: 地址初始化
from .tool import reset_key
from .multitree import MultiTree
from collections.abc import Iterable
import ahocorasick
import bz2
import os
import json
import re
import itertools


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

        删除不支持一串顺序地址删除：例如：贵州省-贵阳市-遵义市
        """
        if isinstance(words, str):
            words = words.strip()  # 去除空格
            if os.path.exists(words):
                with open(words, encoding='UTF-8')as fp:
                    for word in fp:
                        self.delete_vague_text(word)
            else:
                self.ac.remove_word(words)
        elif isinstance(words, Iterable):
            for word in words:
                self.delete_vague_text(word)

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
            words = words.strip()  # 去除空格
            if os.path.exists(words):  # 判断是否存在该文件
                with open(words, encoding='UTF-8')as fp:
                    for word in fp:
                        self.add_vague_text(word, separators)
            elif separators in words:  # 判断是否带有分割符
                self.root.add_value(words, self.ac, separators)
            else:  # 纯字符串
                m = MultiTree(value=words, parent=None)
                self.flag_ac_contain_key(words, m)
        elif isinstance(words, Iterable):  # 迭代器
            for word in words:
                self.add_vague_text(word, separators)

    def _unzip(self) -> (list, dict):
        """解压地址数据包"""
        name = 'address'
        bz = bz2.BZ2File(os.path.dirname(__file__) + os.sep + name + '.bz2')
        lines = bz.read().decode('utf-8')
        address = json.loads(lines[512:-1134], encoding='utf8')
        root = MultiTree(value='中国', parent=None)
        for one_k, one_v in address.items():
            one = MultiTree(value=one_k, parent=root)
            root.add_children(one)
            self.flag_ac_contain_key(one_k, one)
            for two_k, two_v in one_v.items():
                two = MultiTree(value=two_k, parent=one)
                one.add_children(two)
                self.flag_ac_contain_key(two_k, two)
                for three_k, three_v in two_v.items():
                    three = MultiTree(value=three_k, parent=two)
                    two.add_children(three)
                    self.flag_ac_contain_key(three_k, three)
                    for four_k, four_v in three_v.items():
                        four_k = reset_key(four_k)
                        four = MultiTree(value=four_k, parent=three)
                        three.add_children(four)
                        self.flag_ac_contain_key(four_k, four)
                        for five_k in four_v:
                            five_k = reset_key(five_k)
                            five = MultiTree(value=five_k, parent=four)
                            four.add_children(five)
                            self.flag_ac_contain_key(five_k, five)
        return root

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

    def flag_ac_contain_key(self, key, obj):
        """判断ac自动机里面是否包含相同的key值"""
        stop_key = re.sub(self.suffix_stop, '', key)  # 包含一些停用词
        flag = True if len(stop_key) <= 1 else (stop_key == key)
        if key not in self.ac:
            flag or self.ac.add_word(stop_key, [obj])
            self.ac.add_word(key, [obj])
        else:
            flag or self.ac.get(stop_key).append(obj)
            self.ac.get(key).append(obj)
