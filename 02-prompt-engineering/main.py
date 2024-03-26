import os
from openai import OpenAI
import ast
import json

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
env_model = environ_vars["model3"]
env_response_format = environ_vars["response_json"]
env_max_tokens = environ_vars["token1000"]


# 定义多轮会话历史
chat_history = []


# 定义打印消息函数
def print_json(msglist):
    if hasattr(msglist, "model_dump_json"):
        msg = json.loads(msglist.model_dump_json())
    if isinstance(msglist, (list, dict)):
        print(json.dumps(msglist, indent=4, ensure_ascii=False))
    else:
        print(msg)


# 定义chat对话函数
def get_completion(
    roles,
    prompt,
):
    # messages = [{"role": roles, "content": prompt}]
    chat_history.append({"role": roles, "content": prompt})
    response = client.chat.completions.create(
        model=env_model,
        messages=chat_history,
        response_format={"type": env_response_format},
        max_tokens=env_max_tokens,
    )
    print(response.choices[0].message.content)
    # print(response)
    msg = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": msg})
    return response
    # return response.choices[0].message.content


# 定义初始化生成prompt函数
def init_prompt(
    init_roles="",
    instruction="",
    one_shot_learn="",
    output_format="json_object",
):
    # init_roles 定义角色，instruction 任务描述指令, output_format 输出格式约定, input_text 用户输入内容, one_shot_lear 举例,
    # context 上下文即任务背景（多轮会话历史）
    # output_format,input_text,one_shot_learn,context参数指定默认值为""
    prompt = f"""
        {init_roles}


        你的任务是:
        {instruction}


        要求输出的格式为:
        {output_format}


        下面的内容是可供参考的示例,如果参考示例为空请忽略:
        {one_shot_learn}
----EOF-----

        NO COMMENTS. NO ACKNOWLEDGEMENTS
        Let’s think step by step.
        Let’s think step by step.
        Let’s think step by step.
    """
    return prompt


init_roles = "你是一位资深电信客户服务人员"

instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。每种流量套餐产品包含三个属性：名称，月费价格，月流量。根据用户输入，识别用户在上述三种属性上的倾向。请使用中文回答。
"""
output_format = """以 JSON 格式输出"""

one_shot_learn = """"""

# 生成prompt
# 在函数调用时显式地指定参数的名称，从而不受参数顺序的限制
init_prompt_string = init_prompt(
    init_roles=init_roles,
    instruction=instruction,
    output_format=output_format,
    one_shot_learn=one_shot_learn,
)

# userInput = "你是基于哪个模型训练出来的,请使用JSON答复"
get_completion("system", init_prompt_string)

get_completion("user", "办个100G的套餐")

print("----------------")
print(chat_history)
print("----------------")
print_json(chat_history)
