# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/5/7 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  flask 启动
import json
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyunit_address import AddressType

docs_url = os.environ.get('DOCS', "/docs")
app = FastAPI(title='地址抽取', description='基于规则抽取、地址抽取接口文档', version='1.0', docs_url=docs_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
address = AddressType()


class ResponseModal(BaseModel):
    """返回格式类型"""
    msg: str = 'success'
    code: int = 200
    result: list = []


@app.get('/pyunit/address/find', description='查找地址接口', response_model=ResponseModal)
def correct(data: str = Query(..., description='输入一句话')):
    try:
        result = address.address_message(data)
        return ResponseModal(result=result)
    except Exception as e:
        return ResponseModal(code=0, msg=str(e))


@app.get('/pyunit/address/add', response_model=ResponseModal)
def adds(data: str = Query(..., description="增加地址，有顺序的地址用-分开。地址的格式：['贵州省-贵阳市-观山湖区-观山湖公园', '金融大街']")):
    try:
        words = json.loads(data)
        if isinstance(words, list):
            address.add_vague_text(words, '-')
            return ResponseModal(msg='add success')
        else:
            return ResponseModal(code=400, msg='data not is list')
    except Exception as e:
        return ResponseModal(code=0, msg=str(e))


@app.get('/pyunit/address/del', response_model=ResponseModal)
def delete(data: str = Query(..., description="删除地址。地址的格式：['金融大街']")):
    try:
        words = json.loads(data)
        if isinstance(words, list):
            address.delete_vague_text(words)
            return ResponseModal(msg='del success')
        else:
            return ResponseModal(code=400, msg='data not is list')
    except Exception as e:
        return ResponseModal(code=0, msg=str(e))
