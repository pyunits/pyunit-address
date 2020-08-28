# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/5/7 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  flask 启动
import json

from flask import Flask, jsonify, request
from pyaxe_flask import flask_request

from pyunit_address import AddressType

app = Flask(__name__)
address = AddressType()


@app.route('/')
def hello():
    return jsonify(code=200, result='welcome to pyunit-address')


@app.route('/pyunit/address/find', methods=['POST', 'GET'])
def correct():
    try:
        data = flask_request(request)
        word = data['data']
        result = address.address_message(word)
        return jsonify(code=200, result=result)
    except Exception as e:
        return jsonify(code=500, error=str(e))


@app.route('/pyunit/address/add', methods=['POST', 'GET'])
def adds():
    try:
        data = flask_request(request)
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
        data = flask_request(request)
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
