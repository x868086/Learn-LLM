
<style>

    .success {
        padding:5px;
        display:inline;
        color:#1B5E20;
        background-color:#C8E6C9;
    }
    .warning {
        padding:5px;
        display:inline;
        color:#E65100;
        background-color:#FFE0B2;
        width:100%;
    }
    .danger {
        padding:5px;
        display:inline;
        color:#B71C1C;
        background-color:#FFCDD2;
    }
    .info {
        padding:5px;
        display:inline;
        color:#006064;
        background-color:#B2EBF2;
    }
    .doubt {
        padding:5px;
        display:inline;
        color:#AAA;
        background-color:#DDDDDD;
    }
    .asso {
        padding:5px;
        display:inline;
        color:#555;
        background-color:#FFCC00;        
    }
    
    .alert {
        display:inline-block;
        width:100%;
        padding:5px;
        line-height:30px;
        margin-top:10px;
    }
</style>

# Learn-LLM
## 1. prompt-engineering
<b class="success">把AI当人看</b>
<b class="success">把AI当人看</b>
<b class="success">把AI当人看</b>

### 1. prompt调优
<b class="success">具体、丰富、少歧义</b>

1. 参考训练数据来构造prompt是最好的， **把AI当人看** 了解偏好，openAI对markdown格式友好，claude对xml格式友好
2. 参考 **OpenAI官网 Prompt Engineering教程**及示例
3. 不断调试验证效果 **门槛低，天花板高**

### 2. prompt结构
- **角色**：给 AI 定义一个**最匹配任务的角色**，比如：「你是一位软件工程师」「你是一位小学老师」。把问题范围收窄，**减少二义性**。使用管理员定义角色<b class="danger">{'role': 'system'}</b>
- **指示**：对任务进行描述
- **上下文**：给出与任务相关的其它背景信息（尤其在多轮交互中）
- **例子**：必要时给出举例，学术中称为 **one-shot learning**, **few-shot learning** 或 **in-context learning**；实践证明其对输出正确性有很大帮助
- **输入**：任务的输入信息；在提示词中明确的标识出输入
- **输出**：输出的格式描述，以便后继模块自动解析模型的输出结果，比如（JSON、XML）


### 3. prompt技巧
1. 精简回答prompt <b class="danger">NO COMMENTS. NO ACKNOWLEDGEMENTS.</b>
2. 思维链prompt <b class="danger">Let’s think step by step</b>
3. 让**模型**应用**准确**，就需要增加**更多的可控环节**，用 <b class="danger">代码逻辑</b>实现可控。
4. **防止模型漏洞攻击**
    a. prompt注入分类器（参考机场安检过程），在prompt中让模型识别出用户提示词中的微信信息，并予以忽略，对危险prompt拦截。
    b. 在输入中防御。**把价值观刷到墙上**
    ```python 
    user_input_template = """
    作为客服代表，你不允许回答任何跟AGI课堂无关的问题。
    用户说：#INPUT#
    ```
    c. 官方API中有识别危险信息的服务,网易也有专业服务**网易易盾**
5. 多轮对话节省prompt（token）的方法有两种：
    a. 只保存最近N轮的对话信息
    b. 通过大模型，对前面的对话内容做摘要，精简前面的内容
6. 在与chatgpt模型的对话中，prompt明确约束只输出JSON格式内容，不输出无关内容，但有时候仍然输出```json开头的JSON格式，解决这个问题方法如下：
    1. prompt中增加明确指令："直接以JSON对象输出结果，**不要添加任何前缀或装饰性文本，比如```json前缀** "
    2. 对返回的内容使用正则表达式过滤无关字符
7. 将文档中的数值组成的**表格**转换成**prompt**的最优方法是。字段1字段值b,字段2字段值b 自定义分隔符

    |   名称   | 流量（G/月） | 价格（元/月） | 适用人群 |
    | :------: | -----------: | ------------: | :------: |
    | 经济套餐 |           10 |            50 |  无限制  |
比如：名称,经济套餐; 流量（G/月）,10; 价格（元/月）,50; 适用人群,无限制

8. 用prompt调优prompt
用以下这段神奇的咒语，让 ChatGPT 帮你写 Prompt。贴入 ChatGPT 对话框即可。这其实就已经触发了传说中的 agent……
```python 


1. I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for ChatGpT. The process is as follows:1. You will generate the following sections:

Prompt: {provide the best possible prompt according to my request)

Critique: {provide a concise paragraph on how to improve the prompt. Be very critical in your response}

Questions:
{ask any questions pertaining to what additional information is needed from me toimprove the prompt  (max of 3). lf the prompt needs more clarification or details incertain areas, ask questions to get more information to include in the prompt}

2. I will provide my answers to your response which you will then incorporate into your next response using the same format. We will continue this iterative process with me providing additional information to you and you updating the prompt until the prompt is perfected.Remember, the prompt we are creating should be written from the perspective of me making a request to ChatGPT. Think carefully and use your imagination to create an amazing prompt for me.
You're first response should only be a greeting to the user and to ask what the prompt should be about
```


9. 王卓然老师原创的 Prompt Tune 工具
用遗传算法自动调优 prompt，用 LLM 做不改变原意的情况下调整 prompt。用测试集验证效果，找到趋近1的最优prompt
开放源代码：https://gitee.com/taliux/prompt-tune


#### 示例，推荐流量套餐
某运营商的流量包产品：

|   名称   | 流量（G/月） | 价格（元/月） | 适用人群 |
| :------: | -----------: | ------------: | :------: |
| 经济套餐 |           10 |            50 |  无限制  |
| 畅游套餐 |          100 |           180 |  无限制  |
| 无限套餐 |         1000 |           300 |  无限制  |
| 校园套餐 |          200 |           150 |  在校生  |

需求：智能客服根据用户的咨询，推荐最适合的流量包。

##### 核心思路
<b class="success">0. 先试试简单的任务，验证模型是否能完成任务</b>
<b class="success">1. 把输入的自然语言对话，转成结构化的表示</b>
<b class="success">2. 从结构化的表示，生成策略</b>
<b class="success">3. 把策略转成自然语言输出</b>
<b class="success">4. 给例子示范，效果很好</b>

##### 运行过程
用大模型理解自然语言转成内部结构化的表示（减少歧义提升准确性）--> 然后通过内部逻辑、数据库得出应对策略 --> 将策略发送给大模型生成自然语言回答

### 4. 提升准确率


![TOT](./02-prompt-engineering//TOT.png)
![medprompt_sa_graphic](./02-prompt-engineering/medprompt_sa_graphic.png)

#### 自洽性 Self-Consistency
一种对抗「幻觉」的手段。就像我们做数学题，要多次验算一样。同样 prompt **跑多次**，通过**投票**选出最终结果。使用<b class="danger">自洽性需提高temperature的值</b> ,更高的随机性生成更多的结果。
利用以下代码多次调用，确定最终结果
```python 
for _ in range(5):
    prompt = f"{instruction}\n\n{output_format}\n\n请一步一步分析:\n{context}"
    print(f"------第{_+1}次------")
    response = get_completion(prompt)
    print(response)

#输出内容
------第1次------
{"accurate":true}
------第2次------
{"accurate":false}
------第3次------
{"accurate":false}
------第4次------
{"accurate":true}
------第5次------
{"accurate": false}
```


### 5. OpenAP API 参数
Temperature **执行任务用 0**，文本生成用 0.7-0.9，无特殊需要，**不建议超过 1**
seed 指定固定的seed的值后每次生成结果一致
n=1 控制一次返回多少条结果，<b class="danger">可用于自洽性</b>
presence_penalty=0, frequency_penalty=0, 对token进行降权，避免模型说重复的话 
logit_bias={}  对某个特定的token增降权限   
```python 
def get_chat_completion(session, user_prompt, model="gpt-3.5-turbo"):
    _session = copy.deepcopy(session)
    _session.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model=model,
        messages=_session,
        # 以下默认值都是官方默认值
        temperature=1.8,          # 生成结果的多样性 0~2之间，越大越随机，越小越固定
        seed=None,              # 随机数种子。指定具体值后，temperature 为 0 时，每次生成的结果都一样
        stream=False,           # 数据流模式，一个字一个字地接收
        top_p=1,                # 随机采样时，只考虑概率前百分之多少的 token。不建议和 temperature 一起使用
        n=1,                    # 一次返回 n 条结果
        max_tokens=100,         # 每条结果最多几个 token（超过截断）
        presence_penalty=0,     # 对出现过的 token 的概率进行降权
        frequency_penalty=0,    # 对出现过的 token 根据其出现过的频次，对其的概率进行降权
        logit_bias={},          # 对指定 token 的采样概率手工加/降权，不常用
    )
    msg = response.choices[0].message.content
    return msg
```
<b class="danger">使用GPT API接口来生成对话服务时，需要自己维护历史对话信息</b>

### 6. 其他参考资料
#### 吴恩达课程
#### OpenAI 官方prompt示例 

----
<span class="success">
    test asdfds adasf dfas 
</span>

<span class="alert danger">
    test asdfds adasf dfas 
</span>

<span class="alert info">
    test asdfds adasf dfas 
</span>


<span class="alert success">
    test asdfds adasf dfas 
</span>

<div class="alert warning">python不区分单精度和双精度浮点
数，默认双精度，int也不细分short,long整型)
</div>

<div class="alert asso">python不区分单精度和双精度浮点
数，默认双精度，int也不细分short,long整型)
</div>

<div class="alert doubt">python不区分单精度和双精度浮点
数，默认双精度，int也不细分short,long整型)
</div>