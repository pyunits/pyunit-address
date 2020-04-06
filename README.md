# **PyUnit-Address** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## 字符串地址查询,支持自定义地址词库
[![](https://img.shields.io/badge/Python-3.7-green.svg)](https://pypi.org/project/pyunit-address/)


## 安装
    pip install pyunit-address

## 说明
    该算法有两个词库，一个是全国五级地址，统计时间是2019年。这个地址库是默认加载。不能删除也不能替换。
    如果需要提取非规则的地址，则实用深度模型：  https://github.com/PyUnit/pyunit-ner
    建议两者一起使用，互相补足。

## 查询地址
```python
from pyunit_address import Address,find_address

def test():
    address = Address(is_max_address=True)
    
    # 添加词库，可以是一个字符串、可以是列表字符串、可以是词库文件，一个词语占一行
    address.add_vague_text('红花岗')   # 在默认词库上追加地址词库
    address.add_vague_text('贵州省-遵义市-遵义县-虾子镇-乐安村') # 添加补全地址
    address.add_vague_text(['花溪', '贵州省-遵义市-遵义县-虾子镇-乐安村'])  # 加载词库列表，替换默认词库
    address.add_vague_text('自定义词库.txt')  # 加载词库文件，替换默认词库
    af = find_address(address,'我家在贵州遵义红花岗区，你家在贵州贵阳花溪区')
    print(af)

if __name__ == '__main__':
    test()
```

### 自动补全地址:输入一句话
```python
from pyunit_address import Address,supplement_address

def test_supplement_address():
    address = Address(is_max_address=True)
    asu = supplement_address(address,'我家在遵义县') # [贵州省-遵义市-遵义县]
    print(asu)

if __name__ == '__main__':
    test_supplement_address()

```

## TODO
- [x] 自动寻找最长地址长度
- [x] 全国五级地址新词库
- [x] 支持自定义地址词库
- [x] 不支持非规则地址
- [x] 支持地址自动补全
- [x] 支持快速高效搜索


## 预计功能
    下次更新自动纠错地址功能

***
[1]: https://blog.jtyoui.com