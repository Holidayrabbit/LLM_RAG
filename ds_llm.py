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

# 自定义硅基流动大模型类
class CustomLLM_Siliconflow:
    def __call__(self, prompt: str) -> str:
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
    


if __name__ == '__main__':
    # 创建自定义LLM实例
    llm = CustomLLM_Siliconflow()
    
    # # 示例查询：将大象装进冰箱分几步？
    # # print(llm("把大象装进冰箱分几步？"))
	# # 基础版
    # # 定义国家名称
    # country = """朝鲜"""
    
    # # 定义任务模板
    # country_template = """
    # 任务: 输入一个国家，输出国家的首都
    # 语言：中文

    # 按json格式输出，输出格式如下：
    # country_name
    # capital_name

    # 国家: {country_name}
    # """

    # # 使用模板创建提示
    # prompt_template = ChatPromptTemplate.from_template(country_template)
    # messages = prompt_template.format_messages(country_name=country)
    
    # # 获取模型响应
    # response = llm(messages)
    # print(response)  # 打印响应内容

    from langchain.prompts.chat import ChatPromptTemplate

    template = "你是一个翻译助手，可以帮助我将 {input_language} 翻译成 {output_language}."
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template),
    ])

    text = "我带着比身体重的行李，\
    游入尼罗河底，\
    经过几道闪电 看到一堆光圈，\
    不确定是不是这里。\
    "
    messages  = chat_prompt.format_messages(input_language="中文", output_language="英文", text=text)
    output  = llm(messages)
    print(output)

    chain = chat_prompt | llm 
    output  = chain.invoke({"input_language":"中文", "output_language":"英文","text": text})
    print(output)
    
    
    
    # from langchain_core.output_parsers import StrOutputParser

    # output_parser = StrOutputParser()
    # output_parser.invoke(output)
    











