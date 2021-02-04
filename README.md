# **PyUnit-Address** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## 字符串地址查询,支持自定义地址词库

[![](https://img.shields.io/badge/Python-3.7-green.svg)](https://pypi.org/project/pyunit-address/)

## 安装

    pip install pyunit-address

## 说明

    该算法有两个词库，一个是全国五级地址，统计时间是2019年。这个地址库是默认加载。不能删除也不能替换。
    如果需要提取非规则的地址，则实用深度模型：  https://github.com/PyUnit/pyunit-ner
    建议两者一起使用，互相补足。

## 测试

```python
from pyunit_address import *
import time

address = Address(is_max_address=True)
address.add_vague_text(['红花岗', '花溪'])  # 加入地址名称
address.add_vague_text('贵州省-遵义市-遵义县-虾子镇-乐安村-乐石台')  # 加入一串有顺序的地址
address.add_vague_text('自定义词库.txt')  # 加载词库文件,词库文件中的每一行，可以是一串顺序地址，也可以是一个地址


def all_test():
    string_ = '我家在红花岗，你家在贵州贵阳花溪区,他家在贵州省遵义市花溪区'
    finds = find_address(address, string_)
    for find in finds:
        print()
        print('地址', find)
        print('补全地址', supplement_address(address, find))
        print('纠错地址', correct_address(address, find))
        print('--------------------------')


# 地址 红花岗
# 补全地址 ['贵州省-遵义市-红花岗区']
# 纠错地址 贵州省-遵义市-红花岗区
# --------------------------
# 
# 地址 贵州贵阳花溪区
# 补全地址 ['贵州省-贵阳市-花溪区']
# 纠错地址 贵州省-贵阳市-花溪区
# --------------------------
# 
# 地址 贵州省遵义市花溪区            注：这个地址是错误的
# 补全地址 []                      注：错误的地址无法补全
# 纠错地址 贵州省-贵阳市-花溪区      注：错误的地址被纠正为对的地址
# --------------------------


if __name__ == '__main__':
    start = time.time()
    all_test()
    print(time.time() - start)  # 0.0002001047134399414秒

```

## 查询地址

```python
from pyunit_address import Address, find_address


def test():
    address = Address(is_max_address=True)

    # 添加词库，可以是一个字符串、可以是列表字符串、可以是词库文件，一个词语占一行
    address.add_vague_text('红花岗')  # 在默认词库上追加地址词库
    address.add_vague_text('贵州省-遵义市-遵义县-虾子镇-乐安村')  # 添加补全地址
    address.add_vague_text(['花溪', '贵州省-遵义市-遵义县-虾子镇-乐安村'])  # 加载词库列表，替换默认词库
    address.add_vague_text('自定义词库.txt')  # 加载词库文件，替换默认词库
    af = find_address(address, '我家在贵州遵义红花岗区')
    print(af)


if __name__ == '__main__':
    test()
```

### 自动补全地址:输入一句话

```python
from pyunit_address import Address, supplement_address


def test_supplement_address():
    address = Address(is_max_address=True)
    asu = supplement_address(address, '我家在遵义县')  # [贵州省-遵义市-遵义县]
    print(asu)


if __name__ == '__main__':
    test_supplement_address()
```

### 自动纠正地址

```python
from pyunit_address import Address, correct_address


def correct_address_test():
    address = Address(is_max_address=True)
    print(correct_address(address, '贵州省遵义市花溪区'))  # 贵州省-贵阳市-花溪区


if __name__ == '__main__':
    correct_address_test()
```

## Docker部署

    docker pull jtyoui/pyunit-address
    docker run -d -P pyunit-time

## Swagger在线api文档

    http://localhost:xxx/docs

### 寻找地址的请求参数

|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|data|string|YES|输入一句带有地址的句子|

### 请求示例

> #### Python3 Requests测试

```python
import requests

url = "http://127.0.0.1:2312/pyunit/address/find"
data = {
    'data': '我家在贵州龙里'
}
response = requests.get(url, params=data).json()
print(response)
``` 

> #### 返回结果

```json
{
  "code": 200,
  "result": [
    {
      "address": "龙里",
      "correct_address": "贵州省-黔南布依族苗族自治州-龙里县",
      "supplement_address": [
        {
          "key": "贵州省-黔南布依族苗族自治州-龙里县"
        }
      ],
      "type": "区县"
    }
  ]
}
```

### 增加地址词库请求参数

|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|data|string|YES|输入一句带有地址的句子|

### 请求示例

> #### Python3 Requests测试

```python
import json
import requests

url = "http://127.0.0.1:2312/pyunit/address/add"
data = {
    'data': json.dumps(['贵州省-贵阳市-观山湖区-观山湖公园', '金融大街', '小吃城'])
}
response = requests.get(url, params=data).json()
print(response)
``` 

### 删除地址词库请求参数

|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|data|string|YES|输入一句带有地址的句子|

### 请求示例

> #### Python3 Requests测试

```python
import json

import requests

url = "http://127.0.0.1:2312/pyunit/address/del"
data = {
    'data': json.dumps(['金融大街', '小吃城']),
}
response = requests.get(url, params=data).json()
print(response)
``` 

> #### 返回结果

```json
{
  "code": 200,
  "result": "del success"
}
```

## TODO

- [x] 自动寻找最长地址长度
- [x] 全国五级地址新词库
- [x] 支持自定义地址词库
- [x] 不支持非规则地址
- [x] 支持地址自动补全
- [x] 支持快速高效搜索
- [x] 支持纠错地址

***

[1]: https://blog.jtyoui.com
