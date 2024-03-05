import os
from openai import OpenAI

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务

client = OpenAI()

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "请告诉我你是基于哪个模型训练出来的",
        }
    ],
    # model="gpt-3.5-turbo",
    model="gpt-4-1106-preview"
)


# 获取环变量
# vars = os.environ.get("OPENAI_API_KEY")
# print(vars)


# print(response)
print(response.choices[0].message.content)

