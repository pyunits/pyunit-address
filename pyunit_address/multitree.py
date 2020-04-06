#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/4/4 19:43
# @Author: Jtyoui@qq.com
# @interpret: 多叉树


class MultiTree:
    def __init__(self, value, parent):
        self.parent = parent
        self.value = value
        self.children = []

    def add_children(self, children):
        """增加树的一个节点"""
        self.children.append(children)

    def add_value(self, values: str, ac, separators: str = '-'):
        """给出一条路径

        :param values: 一条路径：比例：'贵州省-遵义市-遵义县-虾子镇'
        :param ac: AC自动机对象
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
                if v in ac:
                    ac.get(v).append(new_cls)
                else:
                    ac.add_word(v, [new_cls])
                cls = new_cls
