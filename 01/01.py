import os

from openai import OpenAI

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 获取环境变量加载openai模型
model3 = os.environ.get("model3")
model4 = os.environ.get("model4")

# 配置 OpenAI 服务

client = OpenAI()

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "你是GPT3还是GPT4?",
        }
    ],
    # model="gpt-3.5-turbo",
    model=model4,
)


# 获取环变量
# vars = os.environ.get("OPENAI_API_KEY")
# print(vars)


# print(response)
print(response.choices[0].message.content)
