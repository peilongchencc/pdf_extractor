# pdf_extractor

抽取pdf中的文本并将结果写入json文件。<br>
- [pdf\_extractor](#pdf_extractor)
  - [支持类型:](#支持类型)
  - [项目运行:](#项目运行)
    - [依赖项安装:](#依赖项安装)
    - [运行指令:](#运行指令)
  - [补充:](#补充)


## 支持类型:

| pdf类型        | 支持     |
|---------------|----------|
| 纯文字         | ✅       |
| 纯含有文字的图片 | ✅       |

> 项目采用如果直接提取的文本较少，则使用OCR从图像中提取文本策略。


## 项目运行:

### 依赖项安装:

ubuntu 安装方式如下:<br>

```bash
sudo apt update
pip3 install pytesseract pdf2image PyPDF2 tqdm
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-chi-sim
sudo apt install poppler-utils

# 设置环境变量
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
echo 'export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/' >> ~/.bashrc
source ~/.bashrc
```

### 运行指令:

```bash
python pdf_extractor.py
```

代码运行后，会默认在当前目录创建一个 `output_json` 文件夹，用于存储转化的json文件。<br>


## 补充:

运行以下代码可查看自己系统 Tesseract OCR 拥有的语言数据文件:<br>

```python
import pytesseract

# 检查可用的语言
print(pytesseract.get_languages(config=''))

# output:
# ['chi_sim', 'eng', 'osd']
```
