#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from .address import Address  # 地址初始化
from .addressType import AddressType  # 得到地址类型
from .correctionAddress import correct_address  # 纠错地址
from .findAddress import find_address  # 查询地址
from .supplementAddress import supplement_address  # 补全地址
from .tool import *

__version__ = '2021.2.4'
__author__ = 'Jtyoui'
__description__ = '全国五级地址查询'
__email__ = 'jtyoui@qq.com'
__names__ = 'pyUnit_address'
__url__ = 'https://github.com/PyUnit/pyunit-address'
