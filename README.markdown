## 环境

- Rust nightly
- Python>=3.7

## 使用方法

- 本机编译
```bash
pip install setuptools-rust, setuptools, wheel

python setup.py build_ext -i # 就地编译
# python setup.py sdist bdist_wheel 打包whl

python3 tests/test.py
```

## 生成pyi注释

```bash
pip install mypy

stubgen -p siomirai # 记得更新对应的rs文件的注释，他们是__doc__的来源

```