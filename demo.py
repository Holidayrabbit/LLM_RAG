import sys
sys.path.append("./") # 将父目录放入系统路径中

# 使用智谱 Embedding API，注意，需要将上一章实现的封装代码下载到本地
from zhipuai_embedding import ZhipuAIEmbeddings
from ds_llm import CustomLLM_Siliconflow

from langchain.vectorstores.chroma import Chroma

from dotenv import load_dotenv, find_dotenv
import os

import os
import openai
from dotenv import load_dotenv, find_dotenv

# 读取本地/项目的环境变量。

# find_dotenv()寻找并定位.env文件的路径
# load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中  
# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())

# 获取环境变量 OPENAI_API_KEY
API_KEY = os.environ['SILICON_FLOW']

from openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.llms.base import LLM  # 添加这行导入
from typing import Any, List, Optional  # 添加这行导入

# 修改自定义硅基流动大模型类
class CustomLLM_Siliconflow(LLM):  # 继承 LLM 基类
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")
        
        # 发送请求到模型
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V2.5",
            messages=[
                {'role': 'user', 
                 'content': f"{prompt}"}  # 用户输入的提示
            ],
        )

        # 打印响应结构，以便调试
        # print("Response structure:", response)

        # 收集所有响应内容
        content = ""
        if hasattr(response, 'choices') and response.choices:
            for choice in response.choices:
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    chunk_content = choice.message.content
                    # print(chunk_content, end='')  # 可选：打印内容
                    content += chunk_content  # 将内容累加到总内容中
        else:
            raise ValueError("Unexpected response structure")

        return content  # 返回最终的响应内容

    @property
    def _llm_type(self) -> str:
        return "custom_siliconflow"

_ = load_dotenv(find_dotenv())    # read local .env file
zhipuai_api_key = os.environ['ZHIPUAI_API_KEY']

# 定义 Embeddings
embedding = ZhipuAIEmbeddings()

# 向量数据库持久化路径
persist_directory = './data_base/vector_db/chroma'

# 加载数据库
vectordb = Chroma(
    persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
    embedding_function=embedding
)

# print(f"向量库中存储的数量：{vectordb._collection.count()}")

# question = "What is chunking, and how does it improve reading speed?"
# docs = vectordb.similarity_search(question,k=3)
# print(f"检索到的内容数：{len(docs)}")

# for i, doc in enumerate(docs):
#     print(f"检索到的第{i}个内容: \n {doc.page_content}", end="\n-----------------------------------------------------\n")

import os 


llm = CustomLLM_Siliconflow()


from langchain.prompts import PromptTemplate

template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说"谢谢你的提问！"。
{context}
问题: {question}
"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                 template=template)

from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vectordb.as_retriever(),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})

# question_1 = "什么是南瓜书？"
# question_2 = "王阳明是谁？"
# question_3 = "What is the core concept of speed reading taught in this book?"


# result = qa_chain({"query": question_3})
# print("大模型+知识库后回答 question_3 的结果：")
# print(result["result"])

def generate_related_questions(context, previous_question):
    prompt = f"""基于以下上下文和用户的上一个问题，生成2个相关的后续问题。这些问题应该与上下文内容直接相关。
    上下文：{context}
    用户上一个问题：{previous_question}
    
    请生成2个相关问题，用中文回答，每个问题都要简短且明确。按照以下格式输出：
    1. [第一个问题]
    2. [第二个问题]
    """
    
    try:
        response = llm(prompt)
        return response
    except Exception as e:
        return "抱歉，生成相关问题时出现错误。"

def format_ai_response(answer, suggested_questions):
    response = f"""
AI 回答：
{answer}

您可能感兴趣的问题：
{suggested_questions}

请直接输入您的问题："""
    return response

def chat_loop():
    welcome_prompt = """欢迎使用知识库增强对话系统！

您可以从以下问题开始：
1. 什么是速读？
2. 如何提高阅读速度？
3. 速读有什么好处？

请输入您的问题（输入 'quit' 或 'exit' 结束对话）："""
    
    print(welcome_prompt)
    
    previous_question = None
    previous_context = None
    
    while True:
        # 获取用户输入
        user_input = input().strip()
        
        # 检查是否退出
        if user_input.lower() in ['quit', 'exit']:
            print("感谢使用，再见！")
            break
        
        # 如果输入为空，继续下一轮
        if not user_input:
            continue
            
        try:
            # 使用 RAG 系统回答问题
            result = qa_chain({"query": user_input})
            
            # 获取当前回答的上下文
            current_context = "\n".join([doc.page_content for doc in result["source_documents"]])
            
            # 生成相关问题建议
            suggested_questions = generate_related_questions(current_context, user_input)
            
            # 格式化并显示回答和推荐问题
            formatted_response = format_ai_response(result["result"], suggested_questions)
            print(formatted_response)
            
            # 更新上一个问题和上下文
            previous_question = user_input
            previous_context = current_context
            
        except Exception as e:
            print(f"\n抱歉，处理您的问题时出现错误：{str(e)}")
            print("\n请重新输入您的问题：")

if __name__ == "__main__":
    chat_loop()