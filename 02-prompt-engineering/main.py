import os
from openai import OpenAI
import ast

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务

client = OpenAI()

# # 获取环变量
# # vars = os.environ.get("OPENAI_API_KEY")

llm_config = os.environ.get("LLM_CONFIGS")
# 将读取的全局变量字符串转换为字典
environ_vars = ast.literal_eval(llm_config)
# print(type(environ_vars["response_format"]))


def get_completion(
    roles,
    prompt,
    configs,
):
    messages = [{"role": roles, "content": prompt}]
    response = client.chat.completions.create(
        model=configs["model"],
        response_format=ast.literal_eval(configs["response_format"]),
        messages=messages,
        max_tokens=500,
    )
    print(response.choices[0].message.content)
    print(response)
    return response
    # return response.choices[0].message.content


#
def generate_prompt(
    instruction, output_format="", input_text="", one_shot_learn="", context=""
):
    # instruction 指令, output_format 输出格式, input_text 用户输入, one_shot_lear 举例, context 上下文
    # output_format,input_text,one_shot_learn,context参数指定默认值为""
    prompt = f"""
        {instruction}
        {output_format}
        {input_text}
        {one_shot_learn}
    """
    print(prompt)
    return prompt


instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。
每种流量套餐产品包含三个属性：名称，月费价格，月流量。
根据用户输入，识别用户在上述三种属性上的倾向。
"""
output_format = """
以 JSON 格式输出
"""
input_text = """
办个100G的套餐。
"""

one_shot_learn = """

"""

context = """

"""

# 生成prompt
# 在函数调用时显式地指定参数的名称，从而不受参数顺序的限制
prompt_string = generate_prompt(
    instruction=instruction,
    output_format=output_format,
    input_text=input_text,
    one_shot_learn=one_shot_learn,
    context=context,
)

# userInput = "你是基于哪个模型训练出来的,请使用JSON答复"
get_completion("user", prompt_string, environ_vars)
