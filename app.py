# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/5/7 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  flask 启动
import json

from flask import Flask, jsonify, request

from pyunit_address import Address, find_address, supplement_address, correct_address

app = Flask(__name__)

address = Address()


def flask_content_type(requests):
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if 'application/x-www-form-urlencoded' == requests.content_type:
            data = requests.form
        else:  # 无法被解析出来的数据
            raise Exception('POST的Content-Type必须是:application/x-www-form-urlencoded')
    elif requests.method == 'GET':
        data = requests.args
    else:
        raise Exception('只支持GET和POST请求')
    data = dict(data)
    is_max_address = data.get('is_max_address', None)
    if is_max_address and is_max_address.lower() == 'false':
        data['is_max_address'] = False
    is_order = data.get('is_order', None)
    if is_order and is_order.lower() == 'false':
        data['is_order'] = False
    ignore_special_characters = data.get('ignore_special_characters', None)
    if ignore_special_characters and ignore_special_characters.lower() == 'false':
        data['ignore_special_characters'] = False
    return data


@app.route('/')
def hello():
    return jsonify(code=200, result='welcome to pyunit-address')


@app.route('/pyunit/address/supplement_address', methods=['POST', 'GET'])
def supplement():
    try:
        data = flask_content_type(request)
        word = data['data']
        is_max_address = data.get('is_max_address', True)
        is_order = data.get('is_order', False)
        find = supplement_address(address, word, is_max_address, is_order)
        return jsonify(code=200, result=find)
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/address/find_address', methods=['POST', 'GET'])
def finds():
    try:
        data = flask_content_type(request)
        word = data['data']
        is_max_address = data.get('is_max_address', True)
        ignore_special_characters = data.get('ignore_special_characters', True)
        find = find_address(address, word, is_max_address, ignore_special_characters)
        return jsonify(code=200, result=find)
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/address/correct_address', methods=['POST', 'GET'])
def correct():
    try:
        data = flask_content_type(request)
        word = data['data']
        find = correct_address(address, word)
        return jsonify(code=200, result=find)
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/address/add', methods=['POST', 'GET'])
def adds():
    try:
        data = flask_content_type(request)
        word = data['data']
        words = json.loads(word)
        if isinstance(words, list):
            separators = data.get('separators', '-')
            address.add_vague_text(words, separators)
            return jsonify(code=200, result='add success')
        else:
            return jsonify(code=400, result='data not is list,add not success')
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/address/del', methods=['POST', 'GET'])
def delete():
    try:
        data = flask_content_type(request)
        word = data['data']
        words = json.loads(word)
        if isinstance(words, list):
            address.delete_vague_text(words)
            return jsonify(code=200, result='del success')
        else:
            return jsonify(code=400, result='data not is list,del not success')
    except Exception as e:
        return jsonify(code=500, error=str(e))


if __name__ == '__main__':
    app.run(port=2312)
