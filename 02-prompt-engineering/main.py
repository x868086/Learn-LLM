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


# 定义chat对话函数
def get_completion(
    roles,
    prompt,
    configs,
):
    messages = [{"role": roles, "content": prompt}]
    # messages = [].append({"role": roles, "content": prompt})
    response = client.chat.completions.create(
        model=configs["model3"],
        messages=messages,
        response_format={"type": configs["response_json"]},
        max_tokens=configs["token1000"],
    )
    print(response.choices[0].message.content)
    # print(response)
    # msg = response.choices[0].message.content
    # messages.append({"role": "assistant", "content": msg})
    return response
    # return response.choices[0].message.content


# 定义生成prompt函数
def init_prompt(
    init_roles="",
    instruction="",
    input_text="",
    one_shot_learn="",
    context="",
    output_format="json_object",
):
    # init_roles 定义角色，instruction 任务描述指令, output_format 输出格式约定, input_text 用户输入内容, one_shot_lear 举例,
    # context 上下文即任务背景（多轮会话历史）
    # output_format,input_text,one_shot_learn,context参数指定默认值为""
    prompt = f"""
        {init_roles}
        ----EOF-----

        你的任务是:
        {instruction}
        ----EOF-----

        要求输出的格式为:
        {output_format}
        ----EOF-----

        下面的内容是用户输入的内容,如果用户输入为空请忽略:
        {input_text}
        ----EOF-----

        下面的内容是可供参考的示例,如果参考示例为空请忽略:
        {one_shot_learn}
        ----EOF-----

        下面的内容是历史对话内容,如果历史对话为空请忽略:
        {context}
        ----EOF-----


        NO COMMENTS. NO ACKNOWLEDGEMENTS
        Let’s think step by step.
        Let’s think step by step.
        Let’s think step by step.
    """
    # print(prompt)
    return prompt


init_roles = "你是一位资深电信客户服务人员"

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
init_prompt_string = init_prompt(
    instruction=instruction,
    output_format=output_format,
    input_text=input_text,
    one_shot_learn=one_shot_learn,
    context=context,
)

# userInput = "你是基于哪个模型训练出来的,请使用JSON答复"
get_completion("user", init_prompt_string, environ_vars)
