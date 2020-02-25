# **PyUnit-Address** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## 字符串地址查询,支持自定义地址词库
[![](https://img.shields.io/badge/Python-3.6-green.svg)](https://pypi.org/project/pyunit-address/)


## 安装
    pip install pyunit-address

## 说明
    该算法有两个词库，一个是全国五级地址，统计时间是2018年。这个地址库是默认加载。不能删除也不能替换。
    另一个词库是地址的简称词库。是可以替换、删除、追加的，默认的简称词库包括全国的省、市级。
    如果需要提取非规则的地址，则实用深度模型：  https://github.com/PyUnit/pyunit-ner
    建议两者一起使用，互相补足。

## 使用
```python
from pyunit_address import Address

def test():
    address = Address(is_max_address=True)
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪区')
    print(af)

if __name__ == '__main__':
    test()
```

### 自定义增加词库
```python
from pyunit_address import Address

def test_add():
    address = Address(is_max_address=True)
    address.add_vague_text('红花岗')   # 在默认词库上追加地址词库
    address.add_vague_text('花溪')
    # address.add_vague_text(['红花岗', '花溪'])   # 在默认词库上追加地址词库
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪')
    print(af)

if __name__ == '__main__':
    test_add()
```

### 自定义加载词库
```python
from pyunit_address import Address

def test_load():
    address = Address(is_max_address=True)
    address.set_vague_text(['红花岗', '花溪'])  # 加载词库列表，替换默认词库
    # address.set_vague_text('自定义词库.txt')  # 加载词库文件，替换默认词库
    af = address.find_address('我家在贵州遵义红花岗区，你家在贵州贵阳花溪')
    print(af)

if __name__ == '__main__':
    test_load()
```

### 自动补全地址
```python
from pyunit_address import Address

def test_supplement_address():
    address = Address(is_max_address=True)
    asu = address.supplement_address('我家在遵义') # 贵州省-遵义市
    print(asu)

if __name__ == '__main__':
    test_supplement_address()

```

# TODO
- [x] 自动寻找最长地址长度
- [x] 全国五级地址新词库
- [x] 支持自定义地址词库
- [x] 不支持非规则地址
- [x] 支持地址自动补全


***
[1]: https://blog.jtyoui.com