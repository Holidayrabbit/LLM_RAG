from langchain.document_loaders.pdf import PyMuPDFLoader

# 创建一个 PyMuPDFLoader Class 实例，输入为待加载的 pdf 文档路径
loader = PyMuPDFLoader("./data_base/knowledge_db/speed-reading-learn-to-read-a-200-page-book-in-1-hour-109026447x-9781090264473/speed-reading-learn-to-read-a-200-page-book-in-1-hour-109026447x-9781090264473.pdf")

# 调用 PyMuPDFLoader Class 的函数 load 对 pdf 文件进行加载
pdf_pages = loader.load()

print(f"载入后的变量类型为：{type(pdf_pages)}，",  f"该 PDF 一共包含 {len(pdf_pages)} 页")

pdf_page = pdf_pages[4]
print(f"每一个元素的类型：{type(pdf_page)}.", 
    f"该文档的描述性数据：{pdf_page.metadata}", 
    f"查看该文档的内容:\n{pdf_page.page_content}", 
    sep="\n------\n")

#数据清洗
import re
pattern = re.compile(r'[^\u4e00-\u9fff](\n)[^\u4e00-\u9fff]', re.DOTALL)

# 循环处理所有页面
for page in pdf_pages:
    page.page_content = re.sub(pattern, lambda match: match.group(0).replace('\n', ''), page.page_content)
    # 如果需要查看清洗后的内容，可以取消下面这行的注释
print(f"清洗后的内容为：\n{pdf_pages[5].page_content}\n")

# 如果需要第二次清洗（去除特殊字符和空格），可以这样写：
# for page in pdf_pages:
#     page.page_content = page.page_content.replace('•', '').replace(' ', '')

#文档分割


''' 
* RecursiveCharacterTextSplitter 递归字符文本分割
RecursiveCharacterTextSplitter 将按不同的字符递归地分割(按照这个优先级["\n\n", "\n", " ", ""])，
    这样就能尽量把所有和语义相关的内容尽可能长时间地保留在同一位置
RecursiveCharacterTextSplitter需要关注的是4个参数：

* separators - 分隔符字符串数组
* chunk_size - 每个文档的字符数量限制
* chunk_overlap - 两份文档重叠区域的长度
* length_function - 长度计算函数
'''
#导入文本分割器
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 知识库中单段文本长度
CHUNK_SIZE = 500

# 知识库中相邻文本重合长度
OVERLAP_SIZE = 50

# 使用递归字符文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=OVERLAP_SIZE
)

split_docs = text_splitter.split_documents(pdf_pages)
print(f"切分后的文件数量：{len(split_docs)}")

print(f"切分后的字符数（可以用来大致评估 token 数）：{sum([len(doc.page_content) for doc in split_docs])}")


