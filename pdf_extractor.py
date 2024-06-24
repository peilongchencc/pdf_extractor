import pytesseract
from pdf2image import convert_from_path
import PyPDF2
import io
import os
import json
from tqdm import tqdm
import unicodedata
from pathlib import Path
from loguru import logger

def preprocess_text(text):
    """
    预处理文本，规范化、去除空格和无用字符。

    Args:
        text (str): 需要预处理的文本。

    Returns:
        str: 预处理后的文本。
    """
    # 统一大小写并规范化,将文本中的英文部分统一为NFKD格式(例如 cafe\u0301 --> café)
    text = unicodedata.normalize('NFKD', text.casefold())
    # 去除空格和无用字符
    text = text.replace(" ", "").strip().replace('\\n', '\n').replace('\\t', '\t')
    # 移除空行并规范每行的空格
    text = "\n".join([' '.join(line.split()) for line in text.split('\n') if line.strip()])
    return text

def extract_text_from_pdf(pdf_file_path):
    """
    从PDF文件中提取文本内容，首先尝试直接提取文本，若文本较少则通过OCR提取。

    Args:
        pdf_file_path (str): PDF文件路径。

    Returns:
        dict: 包含提取的文本内容及元数据的字典。
    """
    pdf_text = ""
    # 打开PDF文件
    with open(pdf_file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        # 遍历每一页，提取文本
        for page in pdf.pages:
            pdf_text += page.extract_text()

    # 如果直接提取的文本较少，则使用OCR从图像中提取文本
    if len(pdf_text) < 100:
        pdf_text = ""
        # 将PDF文件转换为图像
        images = convert_from_path(pdf_file_path)
        for image in images:
            # 使用OCR提取图像中的文本
            image_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='chi_sim')
            # 读取OCR生成的PDF文件
            image_pdf = PyPDF2.PdfReader(io.BytesIO(image_page), strict=False)
            # 遍历每一页，提取文本
            for page in image_pdf.pages:
                pdf_text += page.extract_text()

    # 对提取的文本进行预处理
    pdf_text = preprocess_text(pdf_text)
    # 获取PDF文件的标题和文件名
    title = Path(pdf_file_path).stem
    file_name = Path(pdf_file_path).name

    # 返回提取结果和元数据
    return {"page_content": pdf_text, "metadata": {"source": file_name, "title": title}}

def process_pdfs(input_directory, output_directory, max_files=5000):
    """
    处理指定目录中的PDF文件，并将提取的文本内容保存为JSON文件。

    Args:
        input_directory (str): 输入PDF文件的目录。
        output_directory (str): 输出JSON文件的目录。
        max_files (int, optional): 最大处理的文件数量。默认为5000。

    Returns:
        dict: 最后处理的PDF文件提取的结果。
    """
    # 检查并创建输出目录
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    processed_count = 0

    # 遍历输入目录中的所有文件
    for filename in tqdm(os.listdir(input_directory)):
        if filename.endswith(".pdf"):
            # 获取PDF文件的完整路径
            pdf_file_path = os.path.join(input_directory, filename)
            
            logger.info(f"Processing file: {pdf_file_path}")
            
            # 提取PDF文件中的文本内容
            result = extract_text_from_pdf(pdf_file_path)
            # 设置输出的JSON文件路径
            json_output_path = os.path.join(output_directory, filename.replace(".pdf", ".json"))

            # 将提取结果保存为JSON文件
            with open(json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False)

            logger.info(f"Successfully wrote to {json_output_path}")
            
            # 增加处理文件计数
            processed_count += 1
            # 如果达到最大处理数量则停止
            if processed_count >= max_files:
                break

if __name__ == "__main__":
    # 设置输入和输出目录
    directory_to_bankpdf = "example_data/"
    directory_to_json = "output_json/"
    # 处理PDF文件并将结果存入json文件
    process_pdfs(directory_to_bankpdf, directory_to_json)