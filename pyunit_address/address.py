#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from collections.abc import Iterable
from pyunit_gof import Singleton
import ahocorasick
import bz2
import os
import json
import re
import itertools


@Singleton
class Address:

    def __init__(self, is_max_address=False):
        """初始化

        :param is_max_address: 满足最长地址
        """

        # 加载精准匹配的词库，共40万
        self.suffix_stop = '[省市县区镇]'
        self.ac = ahocorasick.Automaton()
        self.count = itertools.count(0)
        self.is_max_address = is_max_address
        self._unzip()
        self.ls = {}

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
            if os.path.exists(words):
                with open(words, encoding='UTF-8')as fp:
                    for word in fp:
                        self.add_vague_text(word, separators)
            elif separators in words:
                ls = words.split(separators)
                self.flag_ac_contain_key(ls[0])
                for index in range(1, len(ls)):
                    self.flag_ac_contain_key(ls[index], ls[index - 1])
            else:
                self.flag_ac_contain_key(words)
        elif isinstance(words, Iterable):
            for word in words:
                self.add_vague_text(word, separators)

    def flag_ac_contain_key(self, key, value=None):
        """判断ac自动机里面是否包含相同的key值"""
        key = key.rstrip('委会')
        stop_key = re.sub(self.suffix_stop, '', key)
        if len(stop_key) <= 1:
            flag = True
        else:
            flag = stop_key == key
        if key in self.ac:
            values: list = self.ac.get(key)
            if value and (value not in values):
                values.append(value)
                self.ac.add_word(key, values)
                flag or self.ac.add_word(stop_key, values)
        elif value:
            flag or self.ac.add_word(stop_key, [key, next(self.count), value])
            self.ac.add_word(key, [key, next(self.count), value])
        else:
            flag or self.ac.add_word(stop_key, [key, next(self.count)])
            self.ac.add_word(key, [key, next(self.count)])

    def _unzip(self) -> (list, dict):
        """解压地址数据包"""
        name = 'address'
        bz = bz2.BZ2File(os.path.dirname(__file__) + os.sep + name + '.bz2')
        lines = bz.read().decode('utf-8')
        address = json.loads(lines[512:-1134], encoding='utf8')
        for one_k, one_v in address.items():
            self.flag_ac_contain_key(one_k)
            for two_k, two_v in one_v.items():
                self.flag_ac_contain_key(two_k, one_k)
                for three_k, three_v in two_v.items():
                    self.flag_ac_contain_key(three_k, two_k)
                    for four_k, four_v in three_v.items():
                        self.flag_ac_contain_key(four_k, three_k)
                        for five_k in four_v:
                            self.flag_ac_contain_key(five_k, four_k)

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

    def supplement_address(self, address_name, is_max_address=None, is_order=False) -> list:
        """补全地址

        输入零碎的地址信息。补全地址，比如输入：山西孝义,补全为：山西省-吕梁市-文水县-孝义镇

        当参数：is_max_address=False时。默认补全最短地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_max_address=True。补全最长地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇-孝义村委会

        当参数：is_order=False。补全的地址是无序的，比如：孝义山西，也能补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_order=True。补全的地址是有序的，比如：孝义山西，则补全不出。无法在孝义下面找到关于山西的地址字眼。

        :param address_name: 要补全的地址，比如：山西孝义
        :param is_max_address: 是否是最大补全地址，默认是否。
        :param is_order: 地址补全，是否遵守顺序。默认是：无序
        """
        ls = []
        keys = self.max_match_cut(address_name)
        for key in keys:
            self._find_address_node(key)
            address = self.dfs(key)
            ls.extend(address)
        match = list(filter(self.satisfy_filter(keys, is_order), ls))
        ls = self.remove_subset(match)
        if is_max_address is True:
            return [max(ls, key=lambda x: len(x))]
        elif is_max_address is False:
            return [min(ls, key=lambda x: len(x))]
        return ls

    @staticmethod
    def remove_subset(ls: list) -> list:
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

    def _find_address_node(self, value):
        values = self.ac.get(value)
        for node in values[2:]:
            ls = self.ls.setdefault(values[0], [])
            if node not in ls:
                ls.append(node)
            self._find_address_node(node)

    def dfs(self, key):
        """深度搜索算法

        >>> graph = {'乐石台': ['乐安村'], '乐安村': ['虾子镇', '新加坡'], '虾子镇': ['遵义县'], '遵义县': ['遵义市']}
        """
        graph = self.ls
        key = self.ac.get(key)[0]
        stack, flag, ls = [[key, 0]], True, []
        while stack:
            (v, next_child_idx) = stack[-1]
            if (v not in graph) or (next_child_idx >= len(graph[v])):
                if flag:
                    address = '-'.join((i[0] for i in stack[::-1]))
                    ls.append(address)
                flag = False
                stack.pop()
                continue
            next_child = graph[v][next_child_idx]
            stack[-1][1] += 1
            stack.append([next_child, 0])
            flag = True
        self.ls.clear()
        return ls

    @staticmethod
    def satisfy_filter(finds_address, is_order):
        """满足条件的过滤算法
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
