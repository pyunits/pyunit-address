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


def optimization():
    data = """
        我家住在贵阳市观山湖区中天会展城A2组团1栋
        嗯，行好的，观山湖区金朱东路11号贵州金融城11号楼3层哈
        公司在贵阳市观山湖区金融城maxB座贵州小爱机器人有限公司
        我现在在贵阳上班，我想把我之前遵义交的公积金转过来
        花溪区政府里面.那当前的话，鉴于花溪区政府的地址，已经搬至了花溪区两家坡大数据产业园3号楼花溪区政务服务大厅里面。
        白云区，长坡岭国家森林公园，融创中国控股有限公司（楼盘：楼盘名称融创云麓长林），市民来电反映自己在今年9月25日购房已交20000元的定金和首付以及各项手续费用总共79824元，当时有签订认筹合同，市民表示房开公司不允许市民使用公积金贷款购房，市民对此表示不理解，于是向白云区住建局反映，但未解决市民的诉求，市民希望房开允许市民使用公积金贷款购房或者将定金及各项手续费全额退还，请相关职能部门及时处理。
        白云区，融创云麓，长林楼盘，市民来电反映2020年9月30日，在白云区融创云麓长林购置一套房子时被告知不能用公积金组合贷款，于是其没有继续签合同，现在房开不给组合贷款买房，也不明确答复市民的首付款能不能退，一直拖到现在，市民希望尽快协调处理公积金贷款购房事宜，请相关职能部门及时处理。（市民需要职能部门回复）
        经开区，开发大道，融创城，市民来电反映其10月18日去到该处看房，该处告知购买后先商贷，但两年后可以转为公积金贷款，市民便缴纳了2万元的订金，但后来却告知交房需要2年半，交房后再过2年半才能转，当时市民使用微信转账的费用，经开区住建局之前告知市民只能通过协商处理并且告知其融创会与其联系处理问题，市民至今未接到融创处理电话，市民表示自己是被欺骗消费，并且之前协商多次无果，市民持有沟通贷款时录音，市民现要求退换此笔费用，请相关职能部门及时处理。（同案件：2010271053065）
    """.strip().split('\n')
    for line in data:
        print(find_address(address, line.strip()))


if __name__ == '__main__':
    # start = time.time()
    # find_address_test()
    # test_supplement_address()
    # correct_address_test()
    # all_test()
    # print(time.time() - start)
    optimization()
