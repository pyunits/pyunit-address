#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/4 19:43
# @Author: Jtyoui@qq.com
# @site: 多叉树
import threading
from functools import wraps


class MultiTree:
    def __init__(self, value, parent):
        self.parent = parent
        self.value = value
        self.children = []

    def add_children(self, children):
        """增加树的一个节点"""
        self.children.append(children)

    def dfs(self, key, ls):
        """深度搜索算法"""
        if self.value == key:  # 补全地址的相似算法
            ls.append(self)
        else:
            for node in self.children:
                node.dfs(key, ls)

    def search(self, value, link: str = '-') -> list:
        """搜索该值的路径

        :param value: 值
        :param link: 拼接符
        :return: 该值的路径
        """
        dfs_key, values = [], []
        self.dfs(value, dfs_key)
        for node in dfs_key:
            n = []
            while node.parent:
                n.append(node.value)
                node = node.parent
            else:
                values.append(link.join(reversed(n)))
        return values

    def add_value(self, values: str, separators: str = '-'):
        """给出一条路径

        :param values: 一条路径：比例：'贵州省-遵义市-遵义县-虾子镇'
        :param separators: 分割符
        """
        value = values.split(separators)
        cls = self
        while value:
            v = value.pop(0)
            for node in cls.children:
                if node.value == v:
                    cls = node
                    break
            else:
                new_cls = MultiTree(value=v, parent=cls)
                cls.add_children(new_cls)
                cls = new_cls


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


def singleton(cls):
    """单例模式"""
    instance = {}
    _lock = threading.Lock()  # 实现线程锁，增加安全性

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instance:
            with _lock:
                if cls not in instance:
                    instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return wrapper
