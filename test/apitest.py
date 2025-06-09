import os
from dotenv import load_dotenv, find_dotenv

# 读取本地/项目的环境变量。

# find_dotenv() #寻找并定位 .env 文件的路径
# load_dotenv() #读取该 .env 文件，并将其中的环境变量加载到当前的运行环境中  
# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())

# 如果你需要通过代理端口访问，还需要做如下配置
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7899'
# os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7899'



from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("SILICON_FLOW"),base_url="https://api.siliconflow.cn/v1"
)

# 导入所需库
# 注意，此处我们假设你已根据上文配置了 OpenAI API Key，如没有将访问失败
completion = client.chat.completions.create(
    # 调用模型：ChatGPT-3.5
    model="deepseek-ai/DeepSeek-V2.5",
    # messages 是对话列表
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(completion.choices[0].message.content)

