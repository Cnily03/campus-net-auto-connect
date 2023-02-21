# 校园网自动连接

## 使用

使用以下命令查看帮助，默认参数为 `--login`

```bash
python . --help # 使用源文件
./AutoConnect --help # 如果使用编译的二进制文件
```

## 构建

Python 版本：`~3.10.8`

```bash
pip install -r requirements.txt
python build.py
```

处于安全考虑，建议你修改 `config.py` 中的 `AES_KEY_TEXT` 和 `AES_IV_TEXT`
