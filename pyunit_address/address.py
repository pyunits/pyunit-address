#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
try:
    from collections.abc import Iterable
except ModuleNotFoundError:
    from collections import Iterable
from .TreeAlgorithm import dict_create_tree, Singleton
import ahocorasick
import bz2
import os
import json
import re


@Singleton
class Address:

    def __init__(self, is_max_address=False):
        """初始化

        :param is_max_address: 满足最长地址
        """

        # 加载精准匹配的词库，共40万 、  顺序表
        self.address_data, self.sequential_address = self._unzip()
        self.length_all = len(self.address_data)
        self.is_max_address = is_max_address
        self.Tree = dict_create_tree(self.sequential_address)
        self.ac = ahocorasick.Automaton()
        for index, key in enumerate(self.address_data):
            self.ac.add_word(key, (index, key))
        self.ac.make_automaton()

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
        else:
            raise ValueError('删除值错误')
        self.ac.make_automaton()

    def add_vague_text(self, words: [str, Iterable]):
        """增加地址词语

        传入的参数可以是：一个词语、一个列表、一个元组、甚至是一个文件地址，文件地址里面是包含一列一个词语

        格式1： 只增加一个词

        格式2：增加一个列表
        """
        if isinstance(words, str):
            if os.path.exists(words):
                with open(words, encoding='UTF-8')as fp:
                    for word in fp:
                        self.length_all += 1
                        self.ac.add_word(word, (self.length_all, word))
            else:
                self.length_all += 1
                self.ac.add_word(words, (self.length_all, words))
        elif isinstance(words, Iterable):
            for word in words:
                self.length_all += 1
                self.ac.add_word(word, (self.length_all, word))
        else:
            raise ValueError('增加值错误')
        self.ac.make_automaton()

    @staticmethod
    def _unzip() -> (list, dict):
        """解压地址数据包"""
        name = 'address'
        bz = bz2.BZ2File(os.path.dirname(__file__) + os.sep + name + '.bz2')
        lines = bz.read().decode('utf-8')
        address = json.loads(lines[512:-1134], encoding='utf8')
        ls = set()
        for one_k, one_v in address.items():
            ls.add(one_k)
            for two_k, two_v in one_v.items():
                ls.add(two_k)
                for three_k, three_v in two_v.items():
                    ls.add(three_k)
                    for four_k, four_v in three_v.items():
                        ls.add(four_k)
                        for five_k in four_v:
                            ls.add(five_k)
                # 加载模糊匹配的词库
        ls.update([w.strip() for w in open(os.path.dirname(__file__) + os.sep + 'CAT.txt', encoding='UTF-8')])
        return ls, address

    def find_address(self, data: str, is_max_address=True, ignore_special_characters=True) -> list:
        """查找地址

        :param data: 查找地址数据
        :param is_max_address: 是否查找最长地址
        :param ignore_special_characters: 是否去掉特殊字符
        :return: 地址列表
        """
        if ignore_special_characters:
            data = re.sub(r"[!#$%&'()*+,-./:：，。？！；‘’、《》;<=>?@[\]^_`{|}~\s]", '', data)
        ls = []
        for index, (key, value) in self.ac.iter(data):
            ls.append(value)
        ls = self.remove_subset(ls)
        if is_max_address:
            max_address = []
            match = re.sub('|'.join(ls), lambda x: '*' * len(x.group()), data)
            for addr in re.finditer(r'[*]+', match):
                max_address.append(data[addr.start():addr.end()])
            return max_address
        return ls

    def supplement_address(self, address_name, is_max_address=False, is_order=False, is_remove_subset=True) -> list:
        """补全地址

        输入零碎的地址信息。补全地址，比如输入：山西孝义,补全为：山西省-吕梁市-文水县-孝义镇

        当参数：is_max_address=False时。默认补全最短地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_max_address=True。补全最长地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇-孝义村委会

        当参数：is_order=False。补全的地址是无序的，比如：孝义山西，也能补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_order=True。补全的地址是有序的，比如：孝义山西，则补全不出。无法在孝义下面找到关于山西的地址字眼。

        :param address_name: 要补全的地址，比如：山西孝义
        :param is_max_address: 是否是最大补全地址，默认是否。
        :param is_order: 地址补全，是否遵守顺序。默认是：无序
        :param is_remove_subset: 是否移除地址中含有的地址子集，比如：[山西省-吕梁市,山西省,吕梁市]-->[山西省-吕梁市]
        """
        obj = max if is_max_address else min
        ls, finds_address = [], self.find_address(address_name, is_max_address=False)
        ls = [addr for address in finds_address for addr in self.Tree.search_tree_value(address)]
        match = list(filter(self.satisfy_filter(finds_address, is_order), ls))
        if match:
            ls = obj(match, key=lambda x: len(x))
            return [ls]
        elif ls:
            temporary = []
            for temp in finds_address:
                temporary.append(obj(filter(lambda x: temp in x, ls), key=lambda x: len(x)))
            ls = temporary
        if is_remove_subset:
            return self.remove_subset(ls)
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
